import pandas as pd
import xml.etree.ElementTree as ET
import re
import datetime
from sys import exit
import xml.dom as DOM

import tkinter as tk
from tkinter import filedialog

# TODO: make file pickers for selecting CSV files
# root = tk.Tk()
# root.withdraw()
# file_path = filedialog.askopenfilename()
# root.update()

# GET ALL INPUT FILES
dir_in = 'data_in2'
dir_out = 'data_out'
lms_path = 'data_in2/2019-07-18-12-32-33_d43o0sted3.csv'
lms_data = pd.read_csv(lms_path)
lms_data = lms_data.rename(columns=lambda x: x.strip())  # Remove trailing and leading whitespace
list(lms_data)

lesson = 'Florida: MGT 462 '


def is_filtered(ser):
    # filter only Florida data
    cond = ser['Lesson'] == lesson and \
           ser['Lesson Completion'] == 'completed'
    if cond:
        return True
    else:
        return False


## TODO: Filter multiple conditions?? or just one?
lms_data['FilteredInClass'] = lms_data.apply(
    is_filtered, axis=1).astype('bool')  # Create a new field for Filtered...
# is_fl = lms_data['Lesson'] == lesson
is_fil = lms_data['FilteredInClass'] == True  ## Only select rows
lms_fl = lms_data[is_fil]  ## TODO: drop record for josh

## TODO: Get the count?
num_students = lms_fl.shape[0]
# print(lms_fl['Lesson Success'].describe())

# Get only the columns we need
lms_fl_subset = lms_fl.filter(
    items=[
        'Last Name',
        'First Name',
        'Job Title',
        'Street Address',
        'City',
        'State/Province',
        'Postal Code',
        'Primary Phone',
        'Email',
        'Discipline',
        'Government Level',
        'International Status'
        ## note that there are trailing whitespace
    ]
)

# Export a CSV of filtered LMS
# lms_fl_subset.to_csv('data_out/lms_fl_subsetted.csv')

# Build the node for registration which will be appended later...
registration = ET.Element('registration')  # initialize XML node


# row_to_xml
# row: Series representing user data
# this helper function creates a new XML node
# for students, using the selected fields.
# returns: returns null.
def row_to_xml(row):
    new_student = ET.Element('student')
    new_student.set('international', row['International Status'])
    new_student.set('studentfirstname', row['First Name'])
    new_student.set('studentlastname', row['Last Name'])
    new_student.set('studentcity', row['City'])
    new_student.set('studentzipcode', row['Postal Code'])
    new_student.set('studentphone', row['Primary Phone'])
    new_student.set('discipline', row['Discipline'])
    registration.append(new_student)
    # print("Appended record: " + str(row['First Name']))


# This function outputs nothing
# build_registration_xml
# df: data frame representing user data from LMS system
def build_registration_xml(df):
    df.apply(row_to_xml, axis=1)


build_registration_xml(lms_fl_subset)
registration_tree = ET.ElementTree(registration)
# registration_tree.write('data_out/test.xml')

# Next...
# Import ZipGrade data...
eval_path = './data_in2/quiz-Eval-full.csv'
eval_df = pd.read_csv(eval_path, encoding='latin1')
eval_df = eval_df.rename(columns=lambda x: x.strip())
current = eval_df.head(5)
evaldata = ET.Element('evaldata')  # initialize XML node representing set of all evaluations

# df_identifiers = eval_df.filter(  # Filter only the columns we want
#     axis='columns',
#     items=['StudentID'])

df_only_questions = eval_df.filter(  ## Filter columns by regular expressions
    axis='columns',
    regex='Stu[0-9]+')

df_only_likerts = df_only_questions.drop(labels=['Stu24', 'Stu25', 'Stu26', 'Stu27'], axis=1) \
    .fillna(0) \
    .astype(int)
# Join the filtered df's, convert all to integers

df_only_comments = df_only_questions.filter(
    axis='columns',
    regex='Stu[2][4-9]').fillna('')

# df_cleaned = df_identifiers.join(df_only_questions).astype(int)
df_merged_responses = df_only_likerts.join(df_only_comments)

## If the ZipGrade input does not have empty fields for Stu23 to Stu27,
## Just make empty ones...
# df_ready = df_cleaned.assign(  # Create empty fields for written questions...
#     id24='',
#     id25='',
#     id26='',
#     id27='')

#  Rename column names to replace Stu with id
df_rename = df_merged_responses
df_rename_sample = df_merged_responses.sample(n=num_students, random_state=0)  # TODO double-check random sampling
df_rename.columns = [col.replace('Stu', 'id') for col in df_rename.columns]


# make_eval_tree -> Element
# takes in a df with rows corresponding to students.
# each column is a single question. this func returns
# a tree containing a complete XML tree where
# each <evaldata> corresponds to a student and nests <question> nodes
# df: DataFrame representing evaluations
def make_eval_tree(df):
    all_evals = ET.Element('evaluations')

    # make_tree_from_question -> Element
    # q: a Series representing a single question
    def make_element_from_question(qs):
        generated_eval = ET.Element('evaldata')
        for i, v in qs.iteritems():
            # first process id's and values
            id = re.sub(r'id', '', i)
            val = str(v)
            if int(id) > 23:  # Try to cast the id to an integer... might fail with ID's though
                xml_tag_out = ET.Element('comment', attrib={'id': id, 'answer': 'PLACEHOLDER'})
            else:
                xml_tag_out = ET.Element('question')
            # formatting
            # <question id="15" answer="5"/>
            xml_tag_out.set('id', str(id))
            xml_tag_out.set('answer', val)  # important: must cast to strings before setting attributes...
            generated_eval.append(xml_tag_out)  ## append it to the global eval_out
            # print('index: ', i, 'value: ', v)
        all_evals.append(generated_eval)  # don't forget to append the new evaldata to every thing
        return 'ok'  ## technically it shouldn't matter what is returned since we just just apply to iterate over

    df.apply(make_element_from_question, axis=1)  # Apply function to all rows
    print('Finished building XML for evaluations')
    return all_evals


eval_root = make_eval_tree(df_rename)
evaluations_xml = ET.ElementTree(eval_root)

# evaluations_xml.write('data_out/evals-only.xml')

# Read in metadata and use to populate the other XML fields
df_meta = pd.read_csv(dir_in + '/' + 'meta-template.csv')
df_meta = df_meta.rename(columns=lambda x: x.strip()).rename(columns=lambda y: y.lower())


# get_meta -> String
# field: String representing the field to fetch from the lms dataframe
def get_meta(field):
    out_meta = ''
    try:
        out_meta = str(df_meta.get(str(field)).item())
        if out_meta == 'nan':
            return ''
        else:
            return str(df_meta.get(str(field)).item())
    except:
        print("Empty field, returning empty string" + '')
        return ''


# number of people who pass
# completed
# is_passed_class -> Boolean
# in: DF/series representing a class
# check if person passed the class
# TODO: Calculate the number of students who passed
def is_passed_class(inp):
    if inp.loc['Lesson Success'] == 'passed':
        return True
    else:
        return False


# Make other nodes to finish the xml output file
def make_comment():
    el = ET.Element('comment')
    el.set('id', 'placeholder')
    el.set('answer', 'placeholder')
    return el


element_instructorpoc = ET.Element(
    'instructorpoc',
    attrib={'instlastname': get_meta('instructorpoc_instlastname'),
            'instfirstname': get_meta('instructorpoc_instfirstname'),
            'instphone': get_meta('instructorpoc_instphone')})

el_class = ET.Element('class',
                      attrib={
                          'preparerlastname': get_meta('class_preparerlastname'),
                          'preparerfirstname': get_meta('class_preparerlastname'),
                          'batchpreparerphone': get_meta('class_batchpreparerphone'),
                          'batchprepareremail': get_meta('class_batchprepareremail'),
                          'catalognum': get_meta('class_catalognum'),
                          'classtype': get_meta('class_classtype'),
                          'classcity': get_meta('class_classcity'),
                          'classzipcode': get_meta('class_classzipcode'),
                          'classcountry': get_meta('class_classcountry'),
                          'startdate': get_meta('class_startdate'),
                          'enddate': get_meta('class_enddate'),
                          'starttime': get_meta('class_starttime'),
                          'endtime': get_meta('class_endtime'),
                          'numstudent': str(num_students),  ## TODO: count the number of students
                          'trainingmethod': get_meta('class_trainingmethod'),
                          'contacthours': get_meta('class_contacthours'),
                      })
el_class.append(element_instructorpoc)
el_class.append(registration)
el_class.append(eval_root)

el_testaverage = ET.Element(
    'testaverage',
    attrib={'pretest': get_meta('testaverage_pretest'),
            'posttest': get_meta('testaverage_posttest')})

el_trainingprovider = ET.Element('trainingprovider',
                                 attrib={
                                     'tpid': get_meta('trainingprovider_tpid'),
                                     'tpphone': get_meta('trainingprovider_tpphone'),
                                     'tpemail': get_meta('trainingprovider_tpemail')})
el_trainingprovider.append(el_class)
el_trainingprovider.append(el_testaverage)

el_submission = ET.Element('submission')
el_submission.append(el_trainingprovider)


# export_final_xml
# wrapper function to export the xml files at the very end
def export_final_xml():
    # output_filename_scheme() -> String
    # This function set up the file name scheme
    # and returns a string with the appropriate values
    def output_filename_scheme():
        # format for the xml file name is
        # TP_CourseNumber_Date_SequenceNumber.xml
        str_coursenum = get_meta('class_catalognum')
        date_today = datetime.datetime.today()
        str_datetime = date_today.strftime('%m%d%Y')
        return 'NCDP' + '_' + str_coursenum + '_' + str_datetime + '_' + '1'

    export_tree_manifest = ET.Element('Manifest')
    export_tree_manifest.append(el_submission)

    # # TODO: include DOCTYPE programmatically? Otherwise we have to manually insert the DOCTYPE...
    # doctype_submission = DOM.DocumentType
    # doctype_submission.publicId = 'test'
    # treeee = ET.TreeBuilder()
    # treeee.doctype = ['NAMETEST', 'pubidtest', 'systemtest']
    # treeee.start('Manifest', '')
    # treeee.end("tag")
    # outter = treeee.close()
    export_tree_final = ET.ElementTree(export_tree_manifest)
    string_output_filename = 'data_out/' + output_filename_scheme() + '.xml'
    export_tree_final.write(string_output_filename, encoding="utf-8", xml_declaration=True)
    print('Saved RES XML as: ' + string_output_filename)


export_final_xml()
# exit()
