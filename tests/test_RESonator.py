import pytest
import logging

from pathlib import Path

from resonator.RESonator import RESonator
from xml.etree import ElementTree


class TestRESonator:
    """Tests main program entry point."""

    def test_process_job(self, tmp_path):
        """Tests that process_job runs in RESonator.py"""
        test_outfile = tmp_path / Path("final_out.xml")
        txt = RESonator(
            path_lms_in=Path("tests/sampledata/lms_sample.csv"),
            path_metadata_in=Path("tests/metadata-sample.toml"),
            path_eval_in=Path("tests/sampledata/qualtrics_output.xlsx"),
            path_final_out=test_outfile,
        )
        with open(test_outfile, mode="r") as output:
            text = output.readlines()
            assert text is not None, "Output should not be empty"
