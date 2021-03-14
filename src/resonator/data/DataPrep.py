import pandas as pd
import re
import logging


class DataPrep:
    """
    Handles all general data transformations
    """

    def __init__(self):
        logging.info("Instantiated a DataPrep object")

    @classmethod
    def get_course_list(cls, input_lms):
        """
        Returns a list of all lessons
        :return:
        """
        try:
            # Make a list of all the lessons?
            return input_lms["Course"].unique().tolist()
        except:
            raise ValueError("ERROR: Error reading list of lessons")

    @classmethod
    def prep_data_lms(
        cls, input_lms: pd.DataFrame, course: str, remove_users: list
    ) -> pd.DataFrame:
        """Prepare the data for XML transform. Note tbat this function subsets rows by course.

        Args:f
            input_lms (pd.DataFrame): [description]
            course (str): [description]
            remove_users (list): Test users to be filtered out

        Returns:
            pd.DataFrame: [description]
        """
        logging.info(f"Starting prep_data_lms for course: {course}")

        logging.debug("Stripping column names of spaces")
        lms_prefilter = input_lms.rename(columns=lambda x: x.strip())

        logging.debug("Stripping all string fields of trailing spaces")
        lms_prefilter = lms_prefilter.apply(
            lambda x: x.str.strip() if x.dtype == "object" else x
        )

        filtered_completion = lms_prefilter.query(
            "(Course == @course) & (`Course Status` == 'Completed')"
        )

        # TODO: remove implicit dependency
        # self.num_students_completed = lms_fl.shape[0]

        # Drop test users/instructors
        # lms_fl = lms_fl[lms_fl['Last Name'] != 'DeVincenzo']
        filtered_completion = filtered_completion.loc[
            ~input_lms["Username"].isin(remove_users)
        ]
        logging.debug(f"Dropped instructors: {remove_users}")
        # Get only the columns we need
        lms_fl_subset = filtered_completion.filter(
            items=[
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
            ]
        )  # govt needs to be last
        logging.info("Subsetted columns in lms data")

        def recode_by_regex(input_data):
            """

            Takes in a string and replaces it with a recoded version,
            Only returns the acronym in parentheses...
            helper function meant to be used in apply function...

            :param input_data: String
            :return: String
            """
            regex_str = "\([A-Z]+\)"
            regex = re.compile(regex_str)
            # p = re.compile(regex_str)  # parentheses for capture groups
            sr = re.search(pattern=regex, string=input_data)
            captured = sr.group().strip("()")  # remove the parentheses
            return captured

        # Recode values for fields required
        lms_fl_subset["Government Level"] = lms_fl_subset["Government Level"].apply(
            recode_by_regex
        )

        lms_fl_subset["Discipline"] = lms_fl_subset["Discipline"].apply(recode_by_regex)

        # Export a CSV of filtered, cleaned
        # lms_fl_subset.to_csv('data_out/lms_fl_subsetted.csv')
        return lms_fl_subset

    @classmethod
    def prep_data_eval(cls, input_eval: pd.DataFrame) -> pd.DataFrame:
        """Prep eval DataFrame for XML transformation. Only keep the questions, and rename the fields!

        Args:
            input_eval (pd.DataFrame): input dataframe

        Returns:
            [type]: DataFrame ready to be converted to XML
        """
        ## START EVAL PROCESS
        logging.info("Running prep_data_eval")
        subset = input_eval.iloc[:, 19:]
        # Strip annoying column spaces
        subset = subset.rename(columns=lambda x: x.strip())
        new_q_numbers = map(lambda x: f"NQ{x}", list(range(1, 28)))
        subset.columns = new_q_numbers
        # extract the number from col index 0 - 23 for likerts
        subset.iloc[:, 0:23] = subset.iloc[:, 0:23].apply(
            lambda x: x.str.findall("\d")[0]
        )
        return subset
