import pytest
import logging
from pathlib import Path
import resonator.data.DataIO as dl
import resonator.data.XMLGenerator as xmlgen


class TestXmlGenerator:
    """XML generation tests

    Returns:
        [type]: [description]
    """

    @pytest.fixture(scope="class", autouse=True)
    def sample_lms_input(self):
        loader = dl.DataIO()
        path_in = Path(
            "tests/sampledata/LMS Output Example_UserCourseTranscripts_2021-02-26-21-28-46.csv"
        )
        logging.info(f"Using file input: {path_in}")
        file = loader.load_file_disk(path_in)
        return file

    def test_make_class(self, sample_lms_input):
        """Tests the generation of a single class"""
        logging.info(sample_lms_input)
        assert True == True
        pass

    def test_make_instructorpoc(self):
        """test xml generation of instructorpoc"""
        # TODO
        pass

    def test_make_testaverage(self):
        """test xml generation of instructorpoc"""
        # TODO
        pass

    def test_make_trainingprovider(self):
        """test generation of trainingprovider"""
        # TODO
        pass

    def test_make_submission(self):
        """Tests the total generation of an entire submission"""
        assert True == True
        pass

    def test_write_doctype(self):
        """test doctype insertion"""
        pass
