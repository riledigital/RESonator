import resonator.data.DataPrep as DataPrep
import logging


class TestLMSPrep:
    """
    Unit tests for preparing the LMS data
    """

    TARGET_COLUMNS = [
        "International Status",
        "Last Name",
        "First Name",
        "City",
        "Primary Phone",
        "Discipline",
        "Job Title",
        "Street Address",
        "State/Province",
        "Postal Code",
        "Email",
        "Government Level",
    ]

    def test_lms_subset(self):
        """Should properly subset the fields"""
        pass


class TestDataPrepSchedule:
    """
    Unit test for successfully generating schedule XML data
    """

    def test_training_provider(self):
        # tpid
        # tpphone
        # tpemail
        pass

    def test_schedule(self):
        pass


class TestDataPrepSubmission:
    """
    Unit test for generating final RES submission.xml
    """

    def test_submission(self):
        pass
