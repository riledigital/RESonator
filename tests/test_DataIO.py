import resonator.data.DataIO as dl
import logging
from pathlib import Path
import pandas as pd


class TestDataIo:
    """
    Unit test for loading input files
    """

    def test_load_csv_lms(self):
        """
        Test for columns present
        """
        loader = dl.DataIO()
        file = loader.load_file_disk(
            Path(
                "tests/sampledata/LMS Output Example_UserCourseTranscripts_2021-02-26-21-28-46.csv"
            )
        )
        # Target the full columns in this case
        target_columns = pd.Index(
            data=[
                "Full Name",
                "Last Name",
                "Middle Name",
                "First Name",
                "Email",
                "Username",
                "Job Title",
                "Job Class",
                "Street Address",
                "City",
                "State/Commonwealth/ Territory ",
                "Postal Code",
                "Country",
                "Primary Phone",
                "Work Phone",
                "Home Phone",
                "Fax",
                "Mobile Phone",
                "Pager",
                "Other Phone",
                "Employee ID",
                "Status",
                "Language",
                "Local Timezone",
                "Language (ISO Standard)",
                "Local Timezone (ISO Standard)",
                "Group",
                "Supervisor",
                "Organization",
                "Discipline",
                "Government Level",
                "FEMA SID",
                "International Status",
                "How did you hear about NCDP FEMA training?",
                "Code",
                "Course",
                "Credits",
                "Enroll Date",
                "Date End",
                "Course Status",
                "Date Due",
                "Date Completed",
                "Module",
                "Committed Content Type",
                "Session Date/Time",
                "Content Resource",
                "Module Completion",
                "Module Success",
                "Score",
                "Module Timestamp",
                "Module Time",
                "Module Time Minutes",
                "Attempts",
                "Interaction",
                "Interaction Description",
                "Interaction Type",
                "Interaction Timestamp",
                "Interaction Time",
                "Learner Response",
                "Correct Responses",
                "Result",
                "Objective",
                "Objective Score",
                "Objective Completion Status",
                "Objective Success Status",
            ],
            dtype="object",
        )
        assert isinstance(file, pd.DataFrame)
        assert file.columns.array == target_columns.array

    def test_load_csv_eval(self):
        """
        Load the evaluation sample data, and then test for columns present
        """
        loader = dl.DataIO()
        file = loader.load_file_disk(Path("tests/sampledata/qualtrics_output.xlsx"))
        # Target the full columns in this case
        target_columns = pd.Index(
            data=[],
            dtype="object",
        )
        assert isinstance(file, pd.DataFrame)
        assert file.columns.array == target_columns.array
