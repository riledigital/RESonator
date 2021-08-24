import pytest
import logging

from pathlib import Path

from resonator.RESonator import RESonator
from xml.etree import ElementTree
from lxml import etree


class TestRESonator:
    """Tests main program entry point."""

    @pytest.fixture(scope="class", autouse=True)
    def path_lms_in(scope):
        return Path("tests/sampledata/lms_sample.csv")

    @pytest.fixture(scope="class", autouse=True)
    def path_metadata_in(scope):
        return Path("tests/metadata-sample.toml")

    @pytest.fixture(scope="class", autouse=True)
    def path_eval_in(scope):
        return Path("tests/sampledata/qualtrics_output.xlsx")

    def test_process_job(self, tmp_path, path_lms_in, path_metadata_in, path_eval_in):
        """Tests that process_job runs in RESonator.py"""
        test_outfile = tmp_path / Path("final_out.xml")
        txt = RESonator.process_job(
            path_lms_in=path_lms_in,
            path_metadata_in=path_metadata_in,
            path_eval_in=path_eval_in,
            path_final_out=test_outfile,
        )
        # Read the temp file as to not litter
        with open(test_outfile, mode="r") as output:
            text = output.readlines()
            assert text is not None, "Output should not be empty"

    def test_equal_count_emails(
        self, tmp_path, path_lms_in, path_metadata_in, path_eval_in
    ):
        """Test that the count of students is same as count of evaldata tags.

        Args:
            tmp_path ([type]): [description]
            path_lms_in ([type]): [description]
            path_metadata_in ([type]): [description]
            path_eval_in ([type]): [description]
        """
        test_outfile = tmp_path / Path("final_out.xml")
        txt = RESonator.process_job(
            path_lms_in=path_lms_in,
            path_metadata_in=path_metadata_in,
            path_eval_in=path_eval_in,
            path_final_out=test_outfile,
        )

        # open file and parse
        test_root = etree.parse(str(test_outfile.absolute()))
        # measure count of students
        count_student = len(test_root.xpath("//student"))
        # measure count of evaldatas
        count_evals = len(test_root.xpath("//evaldata"))
        assert (
            count_evals == count_student
        ), "Should have same count of <student> to <evaldata>"
