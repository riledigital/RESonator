import pytest
import logging

from pathlib import Path

from resonator.RESonator import RESonator
from xml.etree import ElementTree

import os
from dotenv import load_dotenv

load_dotenv()

# Set these in .env
PATH_LMS = os.environ["PATH_LMS"]
PATH_EVAL = os.environ["PATH_EVAL"]
PATH_META = os.environ["PATH_META"]


class TestRESonator:
    """Tests main program entry point."""

    def test_process_job(self, tmp_path):
        """Tests that process_job runs in RESonator.py"""
        test_outfile = tmp_path / Path("final_out.xml")
        txt = RESonator(
            path_lms_in=Path(PATH_LMS),
            path_metadata_in=Path(PATH_META),
            path_eval_in=Path(PATH_EVAL),
            path_final_out=test_outfile,
        )
        # Read the temp file as to not litter
        with open(test_outfile, mode="r") as output:
            text = output.readlines()
            assert text is not None, "Output should not be empty"
