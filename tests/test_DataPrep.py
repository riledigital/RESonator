import resonator.data.DataIO as ld
from resonator.data.DataPrep import DataPrep
import pandas as pd
from pathlib import Path
import logging

import os
from dotenv import load_dotenv

load_dotenv()

# Set these in .env
PATH_LMS = os.environ["PATH_LMS"]
PATH_EVAL = os.environ["PATH_EVAL"]
PATH_META = os.environ["PATH_META"]


class TestLMSPrep:
    """
    Unit tests for preparing the LMS data
    """

    def test_data_lms(self):
        """Should properly subset the fields"""
        test_users = ["jld2225"]
        loader = ld.DataIO()
        lms_data = loader.load_file_disk(Path(PATH_LMS))
        output = DataPrep.prep_data_lms(
            input_lms=lms_data,
            codes=["MGT462BL"],
            #  "MGT462BLIA", "MGT462BLOH", "MGT462BLMA"],
            remove_users=test_users,
        )

        target_columns = pd.Index(
            data=[
                "International Status",
                "Last Name",
                "First Name",
                "City",
                "Primary Phone",
                "Discipline",
                "Job Title",
                "Street Address",
                "State/Commonwealth/ Territory",
                "Postal Code",
                "Email",
                "Government Level",
            ],
            dtype="object",
        )
        # Check if
        assert (
            output.columns.array == target_columns.array
        ), "Output columns don't match expected"
        assert isinstance(output, pd.DataFrame), "output not a DataFrame"


class TestEvalPrep:
    """
    Unit tests for preparing the LMS data
    """

    def test_data_eval(self):
        """Should properly subset the fields"""
        loader = ld.DataIO()
        lms_data = loader.load_file_disk(Path(PATH_EVAL))
        output = DataPrep.prep_data_eval(lms_data)
        assert output.shape[1] == 27, "Output should have 27 columns"
        assert isinstance(output, pd.DataFrame), "Output should be a DataFrame"
