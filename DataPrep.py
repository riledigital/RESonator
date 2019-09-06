import pandas as pd
import re
import logging

class DataPrep:

    def __init__(self, lms, evalu, meta_path, lesson_filter_str):
        self.pre_data_lms = lms
        self.pre_data_eval = evalu
        self.pre_data_meta = meta_path
        #self.lesson = 'New Jersey: MGT 462 '
        self.lesson_str = str(lesson_filter_str)
        # self.num_students_total = int(self.pre_data_lms.shape[0])
        logging.info('Instantiated a DataPrep object')

    # pre-prepped data
    pre_data_lms = None
    pre_data_eval = None
    pre_data_meta = None

    # Initialize the final data that will be returned by this class
    prepped_data_lms = None
    prepped_data_eval = None
    prepped_data_meta = None

    # GET ALL INPUT FILES
    dir_in = 'data_in'
    dir_out = 'data_out'
    lms_path = 'data_in/2019-07-18-12-32-33_d43o0sted3.csv'
    pre_data_lms = None
    lesson = None
    num_students_total = None
    num_students_completed = None
    lessons_list = None
    lesson_str = 'INITIALIZED_DEFAULT'

    def get_lessons_list(self):
        """
        Returns a list of all lessons
        :return:
        """
        try:
            # Make a list of all the lessons?
            self.lesson_list = self.pre_data_lms['Lesson'].unique().tolist()
            return self.lesson_list
        except:
            Exception('ERROR: Error reading list of lessons')

    def select_specific_lesson(self, new_lesson_str):
        """
        Choose a specific lesson. Call this after initializing the df
        :param new_lesson_str:
        :return:
        """
        self.lesson_str = new_lesson_str
        logging.info('Narrowing lesson to: ' + str(new_lesson_str))

    def prep_data_lms(self):
        logging.info('Starting prep_data_lms')
        lms_prefilter = self.pre_data_lms
        lms_prefilter = lms_prefilter.rename(columns=lambda x: x.strip())
        # lesson_str = 'New Jersey: MGT 462' # Important for selecting course

        lms_fl = lms_prefilter[
            (lms_prefilter['Lesson'] == self.lesson_str)
            & (lms_prefilter['Lesson Completion'] == 'completed')]
        logging.info('Starting prefiltering for lesson: ' + str(self.lesson_str))
        self.num_students_completed = lms_fl.shape[0]

        # Drop Josh's record and other test users/instructors
        # TODO: Do this by hand...
        # logging.info('Droppped instructor')
        # lms_fl = lms_fl[lms_fl['Last Name'] != 'DeVincenzo']

        # Get only the columns we need
        lms_fl_subset = lms_fl.filter(
            items=[
                'International Status',
                'Last Name',
                'First Name',
                'City',
                'Primary Phone',
                'Discipline',
                'Job Title',
                'Street Address',
                'State/Province',
                'Postal Code',
                'Email',
                'Government Level'])  # govt needs to be last
        logging.info('Subsetted columns in lms data')

        def recode_by_regex(input_data):
            """

            Takes in a string and replaces it with a recoded version,
            Only returns the acronym in parentheses...
            helper function meant to be used in apply function...

            :param input_data: String
            :return: String
            """
            regex_str = '\([A-Z]+\)'
            regex = re.compile(regex_str)
            # p = re.compile(regex_str)  # parentheses for capture groups
            sr = re.search(pattern=regex, string=input_data)
            captured = sr.group().strip('()')  # remove the parentheses
            return captured

        # Recode values for fields
        lms_fl_subset['Government Level'] = \
            lms_fl_subset['Government Level'].apply(recode_by_regex)

        lms_fl_subset['Discipline'] = \
            lms_fl_subset['Discipline'].apply(recode_by_regex)

        # Export a CSV of filtered, cleaned
        # lms_fl_subset.to_csv('data_out/lms_fl_subsetted.csv')
        return lms_fl_subset

    def prep_data_eval(self):
        ## START EVAL PROCESS
        logging.info('Running prep_data_eval()')
        input_eval = self.pre_data_eval
        input_eval = input_eval.rename(columns=lambda x: x.strip())

        ## Filter columns by regular expressions
        df_only_questions = input_eval.filter(
            axis='columns',
            regex='Stu[0-9]+')

        df_only_likerts = df_only_questions.drop(
            labels=['Stu24', 'Stu25', 'Stu26', 'Stu27'], axis=1) \
            .fillna(0) \
            .astype(int)  # \
        # .recode()

        # Join the filtered df's, convert all to integers

        df_only_comments = df_only_questions.filter(
            axis='columns',
            regex='Stu[2][4-9]').fillna('')

        # df_cleaned = df_identifiers.join(df_only_questions).astype(int)
        df_merged_responses = df_only_likerts.join(df_only_comments)

        #  Rename column names to replace Stu with id
        df_rename = df_merged_responses
        df_rename.columns = [
            col.replace('Stu', 'id') for col in df_rename.columns]
        df_rename_sampled = df_rename.sample(
            n=self.num_students_completed,
            random_state=0)

        self.prepped_data_eval = df_rename_sampled
        return self.prepped_data_eval

    def prep_data_meta(self):
        """
        returns a df containing the processed metadata df
        :return: self.prepped_data_meta
        """
        logging.info('Reading in metadata file')
        my_meta = pd.read_csv(
            # self.dir_in + '/' + 'meta-template.csv',
            self.pre_data_meta,
            skipinitialspace=True,
            parse_dates=['class_startdate',
                         'class_enddate',
                         'class_starttime',
                         'class_endtime'],
            infer_datetime_format=True,
            encoding='latin1').rename(
            columns=lambda x: x.strip()).rename(
            columns=lambda y: y.lower())
        self.prepped_data_meta = my_meta
        return self.prepped_data_meta
