import pandas as pd
import xml.etree.ElementTree as et
from lxml import etree
import re
import datetime
import logging
from pathlib import Path
import os
import lxml


class XMLGenerator:
    """
    Takes in DataFrames and exports XML data
    """

    def __init__(self):
        """Initializes instance but doesn't really do anything since its stateless..."""
        logging.info("Initialized XML generator instance")

    def get_meta(self, field):
        """
        Quickly returns the metadata field from the LMS dataframe.
        :param field: String representing the field from the lms dataframe
        :return: String
        """
        df_meta = self.in_df_meta
        try:
            out_meta = str(df_meta.get(str(field)).item())
            if out_meta == "nan":
                return ""
            else:
                return str(df_meta.get(str(field)).item())
        except:
            logging.warning("Empty field, returning empty string" + "")
            return ""

    @classmethod
    def make_evaluations(self, df: pd.DataFrame):
        """
        takes in a df with rows corresponding to students.
        each column is a single question. this func returns
        a tree containing a complete XML tree where
        each <evaldata> corresponds to a student
        and nests <question> nodes
        :param df: DataFrame representing evaluations
        :return: none
        """
        all_evals = et.Element("evaluations")

        # make_tree_from_question -> Element
        # q: a Series representing a single question
        def process_row(row):
            generated_eval = XMLGenerator.make_evaldata(row)
            all_evals.append(generated_eval)

        df.apply(process_row, axis=1)  # Apply to all rows

        logging.info("Finished building XML for evaluations")
        return all_evals

    @staticmethod
    def is_passed_class(inp):
        """
        calculates number of people whonumber of people who pass
        :param inp: DataFrame/Series representing a class
        :return: Boolean
        """
        if inp["Lesson Success"] == "passed":
            return True
        else:
            return False

    @classmethod
    def output_filename_scheme(cls, course_num: str):
        """
        This function set up the file name scheme
        and returns a string with the appropriate values
        :return: String
        """
        # format for the xml file name is
        # NCDP_CourseNumber_DateTime
        date_today = datetime.datetime.today()
        str_datetime = date_today.strftime("%m%d%Y")
        return f"NCDP_{course_num}_{str_datetime}"

    def export_final_xml(self):
        """
        wrapper function to export the xml files at the very end
        :return: none
        """

        self.export_tree_final.write(
            self.string_output_file_path, encoding="utf-8", xml_declaration=True
        )

        logging.info("Saved RES XML as: " + self.string_output_file_path)

    def write_doctype(self):
        """
        writes the DOCTYPE string to the first line of the output XML file

        :return:
        """
        logging.info("Writing DOCTYPE to XML file...")
        # Read in the export file, then
        ## https://stackoverflow.com/a/10507291
        insert = '<!DOCTYPE Manifest SYSTEM "submission.dtd">'
        # out_filename = self.out_path + self.output_filename_scheme() + '.xml'
        f = open(self.string_output_file_path, "r")
        contents = f.readlines()
        f.close()
        contents.insert(1, insert)
        f = open(self.string_output_file_path, "w")
        contents = "".join(contents)
        f.write(contents)
        f.close()
        logging.info("Finished writing DOCTYPE string to  file")

    def generate_xml(self, input_eval, input_lms, metadata):
        """
        main entry point for this class. takes 3 df inputs
        and creates an XML file from them
        :param input_lms: DataFrame
        :param input_eval: DataFrame
        :param input_meta: DataFrame
        :return: String
        """
        el_registration = self.make_registration(input_lms)
        el_instructorpoc = self.make_instructorpoc(metadata)
        el_evaluations = self.make_evaluations(input_eval)

        el_class = self.make_el_class(
            metadata, el_registration, el_instructorpoc, el_evaluations
        )

        el_class.append(el_instructorpoc)
        el_class.append(el_registration)
        el_class.append(self.make_testaverage(metadata))

        el_trainingprovider = self.make_trainingprovider(metadata, el_class)
        self.el_submission.append(el_trainingprovider)

        self.export_final_xml()
        self.write_doctype()
        logging.info(
            "Finished generating XML with name: " + str(self.string_output_filename)
        )

    @classmethod
    def make_evaldata(cls, qs) -> list:
        """Generate XML element from a singular DataFrame row
         of question responses

        Args:
            qs (DataFrame): DataFrame with 1 row(!)

        Returns:
            [et.Element]: <evaldata> element with <question> inside
        """
        generated_eval = et.Element("evaldata")
        for i, v in qs.iteritems():  ## Loop through all questions in a row..
            # first process id's and values
            idnumber = re.sub(r"NQ", "", i)
            val = str(v)
            # print('string id casting to int as: ' + str(id))
            if val != "":
                ## If the value is empty, don't make a node for it
                if int(idnumber) >= 24:
                    generated_eval.append(
                        XMLGenerator.make_el_qcomment(
                            node_type="comment", idnum=idnumber, answer=val
                        )
                    )  # append it to the global eval_out
                else:
                    # make_el_qcomment(node_type="question", id=id, answer=val)
                    generated_eval.append(
                        XMLGenerator.make_el_qcomment(
                            node_type="question", idnum=idnumber, answer=val
                        )
                    )  # append it to the global eval_out
                # Don't create a new element if there is no need to
        # TODO move this thing outta here
        # don't forget to append the new evaldata to every thing
        return generated_eval

    @classmethod
    def make_el_qcomment(cls, node_type: str, idnum: str, answer) -> et.Element:
        """
        Make a single q or comment element

        Args:
            node_type (str): [description]
            id (str): [description]
            answer (int): [description]

        Returns:
            [type]: [description]
        """
        return et.Element(node_type, attrib={"id": idnum, "answer": answer})

    @classmethod
    def make_registration(cls, lms_df: pd.DataFrame):
        registration = et.Element("registration")
        for (index, row) in lms_df.iterrows():
            registration.append(cls.make_student(row))
        return registration

    @classmethod
    def make_student(cls, student):
        """
        this helper function creates a new XML node for students
        based on the selected fields.
        :param student: Series representing user data
        :return: none
        """
        new_student = et.Element(
            "student",
            attrib={
                "international": student["International Status"],
                "studentfirstname": student["First Name"],
                "studentlastname": student["Last Name"],
                "studentcity": student["City"],
                "studentzipcode": student["Postal Code"],
                "studentphone": student["Primary Phone"],
                "discipline": student["Discipline"],
                "govnlevel": student["Government Level"],
            },
        )
        logging.info("Created record for: " + str(student["First Name"]))
        return new_student

    @classmethod
    def make_instructorpoc(cls, input_dict: dict):
        """Create XML Element for instructorpoc

        Args:
            input_dict (dict): dictionary containing instructor information.

        Returns:
            etree.Element: Element
        """
        return et.Element(
            "instructorpoc",
            attrib={
                "instlastname": input_dict.get("instructorpoc_instlastname"),
                "instfirstname": input_dict.get("instructorpoc_instfirstname"),
                "instphone": input_dict.get("instructorpoc_instphone"),
            },
        )

    # @classmethod
    # def make_single_el(cls, tag_name, input_dict):
    #     new_dict = {}
    #     for key in input_dict:
    #         new_dict = input_dict.get(key)
    #     el_out = et.Element(tag_name, new_dict)

    @classmethod
    def make_testaverage(cls, input_meta):
        el_testaverage = et.Element(
            "testaverage",
            attrib={
                "pretest": input_meta.get("testaverage_pretest"),
                "posttest": input_meta.get("testaverage_posttest"),
            },
        )
        return el_testaverage

    @classmethod
    def make_trainingprovider(cls, input_meta, el_class):
        el_trainingprovider = et.Element(
            "trainingprovider",
            attrib={
                "tpid": input_meta.get("trainingprovider_tpid"),
                "tpphone": input_meta.get("trainingprovider_tpphone"),
                "tpemail": input_meta.get("trainingprovider_tpemail"),
            },
        )
        el_trainingprovider.append(el_class)
        return el_trainingprovider

    def build_registration_xml(df):
        """
        This function builds the XML node for registration info
        :param df: DataFrame to build XML from
        :return: none
        """
        df.apply(XMLGenerator.make_student, axis=1)
        logging.info("Finished building XML tree for registration data")

    @classmethod
    def make_el_class(
        cls,
        metadata: dict,
        registration: et.Element,
        instructorpoc: et.Element,
        evaluations: et.Element,
    ):
        """Makes a <class> element with constituent elements.

        Args:
            metadata (dict): user-input metadata file
            registration (et.Element): Registration data
            instructorpoc (et.Element: XML element
            evaluations (et.Element): Qualtrics evaluation data

        Returns:
            [type]: [description]
        """
        el_class = et.Element(
            "class",
            attrib={
                "preparerlastname": metadata.get("class_preparerlastname"),
                "preparerfirstname": metadata.get("class_preparerlastname"),
                "batchpreparerphone": metadata.get("class_batchpreparerphone"),
                "batchprepareremail": metadata.get("class_batchprepareremail"),
                "catalognum": metadata.get("class_catalognum"),
                "classtype": metadata.get("class_classtype"),
                "classcity": metadata.get("class_classcity"),
                "classstate": metadata.get("class_state"),
                "classzipcode": metadata.get("class_classzipcode"),
                "startdate": metadata.get("class_startdate"),
                "enddate": metadata.get("class_enddate"),
                "starttime": metadata.get("class_starttime"),
                "endtime": metadata.get("class_endtime"),
                # TODO: Check if this is correct
                # "numstudent": str(len([*registration])),
                "trainingmethod": metadata.get("class_trainingmethod"),
                "contacthours": metadata.get("class_contacthours"),
            },
        )
        # TODO insert instructorpoc, registration, and evaluations
        el_class.append(instructorpoc)
        el_class.append(registration)
        el_class.append(evaluations)
        el_class.append(cls.make_testaverage(metadata))
        return el_class

    @classmethod
    def make_submission(cls, el_trainingprovider):
        el_submission = et.Element("submission")
        el_submission.append(el_trainingprovider)
        return el_submission

    @classmethod
    def make_manifest(el_submission: et.Element) -> et.Element:
        """Creates a Manifest element and wraps the submission in it

        Args:
            el_submission (et.Element): [description]

        Returns:
            et.Element: [description]
        """
        export_tree_manifest = et.Element("Manifest")
        export_tree_manifest.append(el_submission)
        return et.ElementTree(export_tree_manifest)

    @classmethod
    def validate_dtd(cls, input_xml):
        # https://lxml.de/validation.html#id1
        path = Path("src/resonator/data")
        dtd = etree.DTD(str(Path(path / "submission.dtd")))
        result = dtd.validate(input_xml)
        logging.info(dtd.error_log.filter_from_errors())
        return result
