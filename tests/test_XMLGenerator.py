import pytest
import logging
from pathlib import Path
import resonator.data.DataIO as dl
import resonator.data.XMLGenerator as xmlgen
import resonator.data.DataPrep as dp
from xml.etree import ElementTree


class TestXmlGenerator:
    """XML generation tests"""

    @pytest.fixture(scope="class", autouse=True)
    def sample_lms_input(self):
        loader = dl.DataIO()
        path_in = Path("tests/sampledata/lms_sample.csv")
        logging.info(f"Using file input: {path_in}")
        file = loader.load_file_disk(path_in)
        return dp.DataPrep.prep_data_lms(
            file,
            codes=["MGT462BL"],
            remove_users=["jld2225"],
        )

    @pytest.fixture(scope="class", autouse=True)
    def sample_eval_input(self):
        loader = dl.DataIO()
        file = loader.load_file_disk(Path("tests/sampledata/qualtrics_output.xlsx"))
        return dp.DataPrep.prep_data_eval(file)

    @pytest.fixture(scope="class", autouse=True)
    def sample_meta_input(self):
        loader = dl.DataIO()
        file = loader.load_file_disk(Path("tests/sampledata/meta_sample.csv"))
        return dp.DataPrep.prep_data_meta(file)
        pass

    def test_make_student(self, sample_lms_input):
        # make single student
        logging.debug(sample_lms_input)
        student = sample_lms_input.iloc[0, :]
        student_dict = student.to_dict()
        output = xmlgen.XMLGenerator.make_student(student)
        xml_string = ElementTree.tostring(output)
        logging.debug(ElementTree.tostring(output))
        assert output.attrib.get("discipline") == student_dict.get(
            "Discipline"
        ), "Discipline should match"
        assert output.attrib.get("govnlevel") == student_dict.get(
            "Government Level"
        ), "govnlevel should match"
        assert output.attrib.get("studentcity") == student_dict.get(
            "City"
        ), "studentcity should match"
        # TODO: Check international status code
        assert output.attrib.get("international") == student_dict.get(
            "International Status"
        ), "Intl Status should match"
        assert output.attrib.get("studentlastname") == student_dict.get(
            "Last Name"
        ), "Last name should match"
        assert output.attrib.get("studentphone") == student_dict.get(
            "Primary Phone"
        ), "phone should match"
        assert output.attrib.get("studentzipcode") == student_dict.get(
            "Postal Code"
        ), "zip code should match"
        pass

    def test_make_registration(self, sample_lms_input):
        registration = xmlgen.XMLGenerator.make_registration(sample_lms_input)
        assert (
            len([*registration]) == sample_lms_input.shape[0]
        ), "# of elements inside registration should be equivalent to number of students in dataframe"

    def test_make_instructorpoc(self):
        """test xml generation of instructorpoc"""
        sample_instructor = {
            "instructorpoc_instlastname": "Doe",
            "instructorpoc_instfirstname": "Jane",
            "instructorpoc_instphone": "555-555-5555",
        }
        test_element = xmlgen.XMLGenerator.make_instructorpoc(sample_instructor)
        xml_string = ElementTree.tostring(test_element)
        assert test_element.attrib.get("instlastname") == sample_instructor.get(
            "instructorpoc_instlastname"
        ), "Should exist"
        assert test_element.attrib.get("instfirstname") == sample_instructor.get(
            "instructorpoc_instfirstname"
        ), "Should exist"
        assert test_element.attrib.get("instphone") == sample_instructor.get(
            "instructorpoc_instphone"
        ), "Should exist"
        pass

    def test_make_qcomment(self):
        element = xmlgen.XMLGenerator.make_el_qcomment(
            node_type="comment", idnum=1, answer="Answer123"
        )
        assert element.attrib.get("answer") == "Answer123", "Answer should match"
        assert element.attrib.get("id") == 1, "ID should match"
        assert element.tag == "comment", "node type should match"
        pass

    def test_make_evaldata(self, sample_eval_input):
        # TODO: length of children should equal the length of input eval questions
        sample_eval_qs = sample_eval_input.iloc[0, :]
        element_test = xmlgen.XMLGenerator.make_evaldata(sample_eval_qs)
        assert (
            len([*element_test]) == sample_eval_input.shape[1]
        ), "Length should be equal"
        pass

    def test_make_evaluations(self, sample_eval_input):
        element = xmlgen.XMLGenerator.make_evaluations(sample_eval_input)
        assert element[0].tag == "evaldata", "First child should be evaldata"
        assert (
            len([*element]) == sample_eval_input.shape[0]
        ), "Should have matching children count for eval input shape"
        pass

    def test_make_class(self, sample_lms_input):
        """Tests the generation of a single class"""
        logging.info(sample_lms_input)
        element = xmlgen.XMLGenerator.make_el_class()
        assert len([*element]) == 4, "Should have four child elements"
        assert element[0].tag == "instructorpoc", "Should have instructorpoc"
        assert element[1].tag == "registration", "Should have registration"
        assert element[2].tag == "evaluations", "Should have evaluations"
        assert element[3].tag == "testaverage", "Should have testaverage"
        pass

    def test_make_testaverage(self):
        """test xml generation of testaverage"""
        # TODO
        assert False
        pass

    def test_make_trainingprovider(self):
        """test generation of trainingprovider"""
        # TODO
        assert False
        pass

    def test_make_submission(self):
        """Tests the total generation of an entire submission"""
        assert False
        pass

    def test_make_manifest(self):
        assert False
        pass

    def test_write_doctype(self):
        """test doctype insertion"""
        assert False
        pass

    def test_dtd_validate(self):
        import lxml

        sample_submission_path = str(Path("tests/sampledata/submission-sample.xml"))
        sample_submission = lxml.etree.parse(sample_submission_path)
        assert (
            xmlgen.XMLGenerator.validate_dtd(sample_submission) == True
        ), "Should validate"
        pass
