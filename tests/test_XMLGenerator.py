import pytest
import logging
from pathlib import Path
import resonator.data.DataIO as dl
import resonator.data.XMLGenerator as xmlgen
import resonator.data.DataPrep as dp


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
            course="Preparedness Actions to Promote Economic Resilience and Recovery  (#9178)",
            remove_users=["jld2225"],
        )

    def test_make_registration(self, sample_lms_input):
        registration = xmlgen.XMLGenerator.make_registration(sample_lms_input)
        assert (
            len([*registration]) == sample_lms_input.shape[0]
        ), "# of elements inside registration should be equivalent to number of students in dataframe"

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
        """test xml generation of testaverage"""
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
