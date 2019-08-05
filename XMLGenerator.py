import pandas as pd
import xml.etree.ElementTree as ET
import re
import datetime


class XMLGenerator():
    in_df = pd.DataFrame()
    out_df = pd.DataFrame()

    # get_meta -> String
    # field: String representing the field to fetch from the lms dataframe
    def get_meta(self, field):
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
        ## Finally, return the data.

    def __init__(self, inputty):
        print('Initialized XML generator with input' + str(inputty))

    ## main entry point for this class
    def processXML(self, in_df):
        print(in_df)

        evaldata = ET.Element(
            'evaldata')  # initialize XML node representing set of all evaluations

        # Build the node for registration which will be appended later...
        registration = ET.Element('registration')  # initialize XML node

        # row_to_xml
        # row: Series representing user data
        # this helper function creates a new XML node
        # for students, using the selected fields.
        # returns: returns null.
        def row_to_xml(row):
            new_student = ET.Element('student', attrib={
                'international': row['International Status'],
                'studentfirstname': row['First Name'],
                'studentlastname': row['Last Name'],
                'studentcity': row['City'],
                'studentzipcode': row['Postal Code'],
                'studentphone': row['Primary Phone'],
                'discipline': row['Discipline'],
                'govnlevel': row['Government Level']})
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
        def make_element_from_response(qs):
            generated_eval = ET.Element('evaldata')
            for i, v in qs.iteritems():  ## Loop through all questions in a row..
                # first process id's and values
                id = re.sub(r'id', '', i)
                val = str(v)
                # print('string id casting to int as: ' + str(id))
                if val != '':
                    ## If the value is empty, don't make a node for it
                    if int(id) >= 24:
                        xml_tag_out = ET.Element(
                            'comment',
                            attrib={'id': id, 'answer': val})
                        generated_eval.append(
                            xml_tag_out)  # append it to the global eval_out
                    else:
                        xml_tag_out = ET.Element(
                            'question',
                            attrib={'id': id, 'answer': val})
                        generated_eval.append(
                            xml_tag_out)  # append it to the global eval_out
                    # Don't create a new element if there is no need to
            all_evals.append(
                generated_eval)
            # don't forget to append the new evaldata to every thing
            return 'ok'  ## should not matter

        df.apply(make_element_from_response, axis=1)  # Apply to all rows
        print('Finished building XML for evaluations')
        return all_evals

    # Read in metadata and use to populate the other XML fields
    # TODO: Check if parsing dates properyl on input
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
    df_meta = pd.read_csv(
        dir_in + '/' + 'meta-template.csv',
        skipinitialspace=True,
        parse_dates=['class_startdate',
                     'class_enddate',
                     'class_starttime',
                     'class_endtime'],
        infer_datetime_format=True).rename(
        columns=lambda x: x.strip()).rename(
        columns=lambda y: y.lower())

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
        if inp['Lesson Success'] == 'passed':
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
        attrib={
            'instlastname':
                get_meta('instructorpoc_instlastname'),
            'instfirstname':
                get_meta('instructorpoc_instfirstname'),
            'instphone':
                get_meta('instructorpoc_instphone')})

    el_class = ET.Element(
        'class',
        attrib={
            'preparerlastname':
                get_meta('class_preparerlastname'),
            'preparerfirstname':
                get_meta('class_preparerlastname'),
            'batchpreparerphone':
                get_meta('class_batchpreparerphone'),
            'batchprepareremail':
                get_meta('class_batchprepareremail'),
            'catalognum':
                get_meta('class_catalognum'),
            'classtype':
                get_meta('class_classtype'),
            'classcity':
                get_meta('class_classcity'),
            'classstate':
                get_meta('class_state'),
            'classzipcode':
                get_meta('class_classzipcode'),
            'startdate':
                get_meta('class_startdate'),
            'enddate':
                get_meta('class_enddate'),
            'starttime':
                get_meta('class_starttime'),
            'endtime':
                get_meta('class_endtime'),
            'numstudent':
                str(num_students),
            'trainingmethod':
                get_meta('class_trainingmethod'),
            'contacthours':
                get_meta('class_contacthours')})

    el_class.append(element_instructorpoc)
    el_class.append(registration)
    el_class.append(eval_root)

    el_testaverage = ET.Element(
        'testaverage',
        attrib={
            'pretest':
                get_meta('testaverage_pretest'),
            'posttest':
                get_meta('testaverage_posttest')
        })

    el_class.append(el_testaverage)

    el_trainingprovider = ET.Element(
        'trainingprovider',
        attrib={
            'tpid':
                get_meta('trainingprovider_tpid'),
            'tpphone':
                get_meta('trainingprovider_tpphone'),
            'tpemail':
                get_meta('trainingprovider_tpemail')})
    el_trainingprovider.append(el_class)

    el_submission = ET.Element('submission')
    el_submission.append(el_trainingprovider)

    eval_root = make_eval_tree(df_rename_sampled)
    evaluations_xml = ET.ElementTree(eval_root)

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

    # export_final_xml
    # wrapper function to export the xml files at the very end
    def export_final_xml(self):
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
        export_tree_final.write(string_output_filename, encoding="utf-8",
                                xml_declaration=True)
        print('Saved RES XML as: ' + string_output_filename)

    export_final_xml()

    # write_doctype()
    # writes the DOCTYPE string to the first line of the output XML file
    def write_doctype(self):
        # Read in the export file, then
        ## https://stackoverflow.com/a/10507291
        insert = '<!DOCTYPE Manifest SYSTEM "submission.dtd">'
        out_filename = 'data_out/' + output_filename_scheme() + '.xml'
        f = open(out_filename, "r")
        contents = f.readlines()
        f.close()
        contents.insert(1, insert)
        f = open(out_filename, "w")
        contents = "".join(contents)
        f.write(contents)
        f.close()

    write_doctype()
    # exit()
