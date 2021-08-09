import resonator.data.DataIO as ld
from resonator.data.DataPrep import DataPrep
import pandas as pd
from pathlib import Path
import logging


class TestLMSPrep:
    """
    Unit tests for preparing the LMS data
    """

    def test_data_lms(self):
        """Should properly subset the fields"""
        test_users = ["jld2225"]
        loader = ld.DataIO()
        lms_data = loader.load_file_disk(Path("tests/sampledata/lms_sample.csv"))

        eval_path = loader.load_file_disk(
            Path("tests/sampledata/qualtrics_output.xlsx")
        )
        eval_emails = DataPrep.prep_data_eval(eval_path)[1]

        output = DataPrep.prep_data_lms(
            input_lms=lms_data,
            emails=eval_emails,
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
        lms_data = loader.load_file_disk(Path("tests/sampledata/qualtrics_output.xlsx"))
        output = DataPrep.prep_data_eval(lms_data)[0]
        assert output.shape[1] == 27, "Output should have 27 columns"
        assert isinstance(output, pd.DataFrame), "Output should be a DataFrame"
