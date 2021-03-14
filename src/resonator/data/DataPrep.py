import pandas as pd
import re
import logging


class DataPrep:
    """
    Handles all general input and data transformations
    """

    def __init__(self, lms, evalu, meta_path, lesson_filter_str):
        self.pre_data_lms = lms
        self.pre_data_eval = evalu
        self.pre_data_meta = meta_path
        # self.lesson = 'New Jersey: MGT 462 '
        self.lesson_str = str(lesson_filter_str)
        # self.num_students_total = int(self.pre_data_lms.shape[0])
        logging.info("Instantiated a DataPrep object")

    # pre-prepped data
    pre_data_lms = None
    pre_data_eval = None
    pre_data_meta = None

    # Initialize the final data that will be returned by this class
    prepped_data_lms = None
    prepped_data_eval = None
    prepped_data_meta = None

    # GET ALL INPUT FILES
    dir_in = "data_in"
    dir_out = "data_out"
    lms_path = "data_in/2019-07-18-12-32-33_d43o0sted3.csv"
    pre_data_lms = None
    lesson = None
    num_students_total = None
    num_students_completed = None
    lessons_list = None
    lesson_str = "INITIALIZED_DEFAULT"

    def get_lessons_list(self):
        """
        Returns a list of all lessons
        :return:
        """
        try:
            # Make a list of all the lessons?
            self.lesson_list = self.pre_data_lms["Lesson"].unique().tolist()
            return self.lesson_list
        except:
            Exception("ERROR: Error reading list of lessons")

    def select_specific_lesson(self, new_lesson_str):
        """
        Choose a specific lesson. Call this after initializing the df
        :param new_lesson_str:
        :return:
        """
        self.lesson_str = new_lesson_str
        logging.info("Narrowing lesson to: " + str(new_lesson_str))

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
                "State/Province",
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

    def prep_data_meta(self):
        """
        returns a df containing the processed metadata df
        :return: self.prepped_data_meta
        """
        logging.info("Reading in metadata file")
        my_meta = (
            pd.read_csv(
                # self.dir_in + '/' + 'meta-template.csv',
                self.pre_data_meta,
                skipinitialspace=True,
                parse_dates=[
                    "class_startdate",
                    "class_enddate",
                    "class_starttime",
                    "class_endtime",
                ],
                infer_datetime_format=True,
                encoding="latin1",
            )
            .rename(columns=lambda x: x.strip())
            .rename(columns=lambda y: y.lower())
        )
        self.prepped_data_meta = my_meta
        return self.prepped_data_meta
