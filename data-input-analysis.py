import pandas as pd
import xml.etree.ElementTree as ET
import re
import datetime

dir_out = 'data_out'

lms_path = "data_original/2019-07-16-11-01-11_u0apmv5n7p.csv"
lms_data = pd.read_csv(lms_path)
list(lms_data)

# filter only Florida data
selector = 'Florida: MGT 462 '
is_fl = lms_data['Lesson'] == selector
lms_fl = lms_data[is_fl]

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
        'Discipline ',
        'Government Level ',
        'International Status '
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
    new_student.set('international', row['International Status '])
    new_student.set('studentfirstname', row['First Name'])
    new_student.set('studentlastname', row['Last Name'])
    new_student.set('studentcity', row['City'])
    new_student.set('studentzipcode', row['Postal Code'])
    new_student.set('studentphone', row['Primary Phone'])
    new_student.set('discipline', row['Discipline '])
    registration.append(new_student)
    print("Appended record: " + str(row['First Name']))


# This function outputs nothing
# build_registration_xml
# df: data frame representing user data from LMS system
def build_registration_xml(df):
    df.apply(row_to_xml, axis=1)


build_registration_xml(lms_fl_subset)
registration_tree = ET.ElementTree(registration)
registration_tree.write('data_out/test.xml')

# Next...
# Import ZipGrade data...
eval_path = "data_original/quiz-Eval-full (1).csv"
eval_df = pd.read_csv(eval_path)
current = eval_df.head(5)
evaldata = ET.Element('evaldata')  # initialize XML node representing set of all evaluations

df_identifiers = eval_df.filter(  # Filter only the columns we want
    axis='columns',
    items=['StudentID'])
df_only_questions = eval_df.filter(  ## Filter columns by regular expressions
    axis='columns',
    regex='Stu[0-9]+')

df_cleaned = df_identifiers.join(df_only_questions)  # Join the filtered df's
df_ready = df_cleaned.assign(  # Create empty fields for written questions...
    id24='',
    id25='',
    id26='',
    id27='')

#  TODO: Create duplicate columns where question number can be identified?...

#  Rename column names to replace Stu with id
df_rename = df_ready
df_rename.columns = [col.replace('Stu', 'id') for col in df_rename.columns]


# make_eval_tree -> Element
# takes in a df with rows corresponding to students.
# each column is a single question. this func returns
# a tree containing a complete XML tree where
# each <evaldata> corresponds to a student and nests <question> nodes
# df: DataFrame representing evaluations
def make_eval_tree(df):
    all_evals = ET.Element('evaluations')

    # make_tree_from_question
    # q: a Series representing a single question
    def make_tree_from_question(qs):
        generated_eval = ET.Element('evaldata')
        for i, v in qs.iteritems():
            xml_tag_out = ET.Element('question')
            # formatting
            # <question id="15" answer="5"/>
            id = re.sub(r'id', '', i)
            val = str(v)
            xml_tag_out.set('id', str(id))
            xml_tag_out.set('answer', val)  # important: must cast to strings before setting attributes...
            generated_eval.append(xml_tag_out)  ## append it to the global eval_out
            # print('index: ', i, 'value: ', v)
        all_evals.append(generated_eval)  # don't forget to append the new evaldata to every thing
        return 'ok'  ## technically it shouldn't matter what is returned?

    df.apply(make_tree_from_question, axis=1)  # Apply function to all rows
    print('done building evals')
    return all_evals


eval_root = make_eval_tree(df_rename)
evaluations_xml = ET.ElementTree(eval_root)
evaluations_xml.write('data_out/evals-only.xml')


# Make other nodes to finish the xml output file
def make_comment():
    el = ET.Element('comment')
    el.set('id', 'placeholder')
    el.set('answer', 'placeholder')
    return el


element_instructorpoc = ET.Element(
    'instructorpoc',
    attrib={'instlastname': 'PLACEHOLDER',
            'instfirstname': 'PLACEHOLDER',
            'instphone': 'PLACEHOLDER'})

el_class = ET.Element('class',
                      attrib={
                          'catalognum': 'PLACEHOLDER',
                          'classtype': '',
                          'classcity': '',
                          'classzipcode': '',
                          'classcountry': '',
                          'startdate': '',
                          'enddate': '',
                          'starttime': '',
                          'endtime': '',
                          'numstudent': '',
                          'trainingmethod': '',
                          'contacthours': '',
                          'numstudent': ''
                      })
el_class.append(element_instructorpoc)
el_class.append(registration)
el_class.append(eval_root)

el_testaverage = ET.Element(
    'testaverage',
    attrib={'pretest': 'PLACEHOLDER',
            'posttest': 'PLACEHOLDER'})

el_trainingprovider = ET.Element('trainingprovider',
                                 attrib={
                                     'tpid': '',
                                     'tpphone': '',
                                     'tpemail': ''
                                 })
el_trainingprovider.append(el_class)
el_trainingprovider.append(el_testaverage)

el_submission = ET.Element('submission')
el_submission.append(el_trainingprovider)


# Set up the file name scheme...
# output_filename_scheme() -> String
def output_filename_scheme():
    # format for the xml file name is
    # TP_CourseNumber_Date_SequenceNumber.xml
    str_coursenum = 'MGTETC'
    date_today = datetime.datetime.today()
    str_datetime = date_today.strftime('%m%d%Y')
    return 'NCDP-' + str_coursenum + '-' + str_datetime + '-' + '1'


export_tree_final = ET.ElementTree(el_submission)
export_tree_final.write('data_out/' + output_filename_scheme() + '.xml',
                        encoding="utf-8", xml_declaration=True)
