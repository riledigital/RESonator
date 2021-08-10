import pandas as pd
import re
import logging
import pycountry
from fuzzywuzzy import fuzz


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
        cls, input_lms: pd.DataFrame, emails: pd.Series, remove_users: list
    ) -> pd.DataFrame:
        """Prepare the data for XML transform. Note tbat this function subsets rows by email and thus must be run after eval has been processed.

        Args:
            input_lms (pd.DataFrame): [description]
            emails (pd.Series): emails to select. If empty, we select all
            remove_users (list): Test users to be filtered out

        Can fuzzy match on emails if desired
        @see https://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/
        Returns:
            pd.DataFrame: [description]
        """

        logging.debug("Stripping column names of spaces")
        lms_prefilter = input_lms.rename(columns=lambda x: x.strip())

        lms_prefilter.drop_duplicates(subset=["Username"], inplace=True, keep="first")
        logging.info("Dropped duplicate users")

        logging.debug("Stripping all string fields of trailing spaces")
        lms_prefilter = lms_prefilter.apply(
            lambda x: x.str.strip() if x.dtype == "object" else x
        )

        try:
            emails_length = emails.shape[0]
            if emails_length > 0:
                emails_list = emails.to_list()
                email_matches = {k: 0 for k in emails_list}
                logging.info(f"Selecting only emails: {emails_list}")

                def fuzz_match(x):
                    for test_str in emails_list:
                        if test_str == x:
                            # Early return if perfect match
                            email_matches[test_str] += 1
                            return True
                        # else fuzzy match
                        ratio = fuzz.ratio(x, test_str)
                        if ratio > 85:
                            logging.info(f"Matched {x} <-> {test_str}")
                            email_matches[test_str] += 1
                            return True
                        else:
                            pass
                    return False

                mask_codes = lms_prefilter["Email"].apply(fuzz_match)
                unmatched_emails = [k for k, v in email_matches.items() if v < 1]
                if len(unmatched_emails) > 1:
                    logging.info(f"Found unmatched emails: {unmatched_emails}")
                lms_prefilter = lms_prefilter[mask_codes]
            else:
                logging.info(f"No codes specified. Skipping email filtering")
        except Exception as e:
            logging.warn(e)

        filtered_completion = lms_prefilter.query("(`Course Status` == 'Completed')")
        filtered_completion = filtered_completion.loc[
            ~input_lms["Username"].isin(remove_users)
        ]
        logging.info(f"Dropped instructors: {remove_users}")
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

        lms_fl_subset["International Status"] = lms_fl_subset[
            "International Status"
        ].str[0]

        def recode_subdivisions(input: str):
            """Recodes state code by lookup

            Args:
                input (str): Input country string
            """
            if len(input) > 2:
                # test_str = input.split(" ")[0]
                subdivisions = pycountry.subdivisions
                try:
                    nomenclature = subdivisions.lookup(input)
                    return nomenclature.code[:2]
                except LookupError as err:
                    logging.error(f"'State/Commonwealth/ Territory' not found: {err}")
                    return input
            else:
                return input

        def recode_country(input: str):
            """Recodes country code by lookup, unused?

            Args:
                input (str): Input country string
            """
            if len(input) > 2:
                return pycountry.countries.lookup("United States").alpha_2
            else:
                return input

        def recode_by_regex(input_data):
            """

            Takes in a string and replaces it with a recoded version,
            Only returns the acronym in parentheses...
            helper function meant to be used in apply function...

            :param input_data: String
            :return: String
            """
            regex_str = r"\([A-Z]+\)"
            regex = re.compile(regex_str)
            # p = re.compile(regex_str)  # parentheses for capture groups
            sr = re.search(pattern=regex, string=input_data)
            captured = sr.group().strip("()")  # remove the parentheses
            return captured

        # Recode State values
        # lms_fl_subset["State/Commonwealth/ Territory"] = lms_fl_subset[
        #     "State/Commonwealth/ Territory"
        # ].apply(recode_subdivisions)

        # Recode values for fields required
        lms_fl_subset["Government Level"] = lms_fl_subset["Government Level"].apply(
            recode_by_regex
        )

        lms_fl_subset["Discipline"] = lms_fl_subset["Discipline"].apply(recode_by_regex)

        # Export a CSV of filtered, cleaned
        # lms_fl_subset.to_csv('data_out/lms_fl_subsetted.csv')
        return lms_fl_subset

    @classmethod
    def prep_data_eval(cls, input_eval: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        """Prep eval DataFrame for XML transformation. Only keep the questions, and rename the fields!

        Args:
            input_eval (pd.DataFrame): input dataframe

        Returns:
            [tuple]: DataFrame ready to be converted to XML, and a pd.Series
        """
        ## START EVAL PROCESS
        logging.info("Running prep_data_eval")
        labels = [
            # "Q1",
            # "Q2",
            # Only start likerts with Q3_1
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
            # TODO: Possibly use QID26 to join on students and subset properly
            "QID26",
        ]
        # Save emails to another col
        s_emails = input_eval.copy().loc[:, "QID26"]
        # Drop emails
        subset = input_eval.copy().loc[:, labels]
        subset.drop("QID26", axis=1, inplace=True)
        new_q_numbers = list(map(lambda x: f"NQ{x}", list(range(1, 28))))
        subset.columns = new_q_numbers

        # extract the number from col index 0 - 23 for likerts
        recoded = subset.iloc[:, 0:23]
        recoded = recoded.applymap(
            lambda x: re.findall(r"\d", x)[0],
        )
        subset.update(recoded)
        # Fill empty/null with empty string
        subset.fillna("NA", inplace=True)
        return (subset, s_emails)

    @classmethod
    def prep_data_meta(cls, input_meta: pd.DataFrame) -> pd.DataFrame:
        # Transform/correct data if necessary, otherwise return input_meta
        return input_meta
