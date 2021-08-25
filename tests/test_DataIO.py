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
        file = loader.load_file_disk(Path("tests/sampledata/lms_sample.csv"))
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
        assert isinstance(file, pd.DataFrame), "Output should be a DataFrame"
        assert (
            file.columns.array == target_columns.array
        ), "Output should match expected columns"

    def test_load_eval(self):
        """
        Load the evaluation sample data, and then test for columns present
        """
        loader = dl.DataIO()
        file = loader.load_file_disk(Path("tests/sampledata/qualtrics_output.xlsx"))
        # Target the full columns in this case
        target_columns = pd.Index(
            data=[
                "StartDate",
                "EndDate",
                "Status",
                "IPAddress",
                "Progress",
                "Duration (in seconds)",
                "Finished",
                "RecordedDate",
                "ResponseId",
                "RecipientLastName",
                "RecipientFirstName",
                "RecipientEmail",
                "ExternalReference",
                "LocationLatitude",
                "LocationLongitude",
                "DistributionChannel",
                "UserLanguage",
                "Q1",
                "QID26",
                "Q2",
                "Q3_1",
                "Q3_2",
                "Q4_1",
                "Q4_2",
                "Q4_3",
                "Q4_4",
                "Q5_1",
                "Q5_2",
                "Q5_3",
                "Q5_4",
                "Q5_5",
                "Q5_6",
                "Q5_7",
                "Q5_8",
                "Q6_1",
                "Q6_2",
                "Q6_3",
                "Q6_4",
                "Q6_5",
                "Q7_1",
                "Q7_2",
                "Q7_3",
                "Q7_4",
                "Q8",
                "Q9",
                "Q10",
                "Q11",
            ],
            dtype="object",
        )
        test_cols = file.columns
        assert isinstance(file, pd.DataFrame), "Output should be a DataFrame"
        assert list(test_cols.array) == list(
            target_columns.array
        ), "Output should match expected columns"

    def test_load_toml_meta(self):
        """
        Load the metaata sample data, and then test for columns present
        """
        loader = dl.DataIO()
        file = loader.load_toml(Path("tests/metadata-sample.toml"))
        # Target the full columns in this case
        target_keys = [
            "trainingprovider_tpid",
            "trainingprovider_tpphone",
            "trainingprovider_tpemail",
            "class_catalognum",
            "class_classtype",
            "class_classcity",
            "class_classzipcode",
            "class_classcountry",
            "class_startdate",
            "class_enddate",
            "class_starttime",
            "class_endtime",
            "class_trainingmethod",
            "class_contacthours",
            "testaverage_pretest",
            "testaverage_posttest",
            "instructorpoc_instlastname",
            "instructorpoc_instfirstname",
            "instructorpoc_instphone",
            "instructorpoc_instemail",
            "class_preparerlastname",
            "class_preparerfirstname",
            "class_preparerphone",
            "class_batchprepareremail",
        ]
        target_keys.sort()
        actual_keys = file.keys()
        assert isinstance(file, dict), "Output should be a dict"
        assert all(
            field in actual_keys for field in target_keys
        ), "Output should match expected keys"
