import pandas as pd
import re
from sys import exit

class DataPrep():
    # Initialize the final data that will be returned by this class
    prepped_data_lms = pd.DataFrame()
    prepped_data_eval = pd.DataFrame()
    prepped_data_meta = pd.DataFrame()

    # GET ALL INPUT FILES
    dir_in = 'data_in2'
    dir_out = 'data_out'
    lms_path = 'data_in2/2019-07-18-12-32-33_d43o0sted3.csv'
    lms_data = ''
    lesson = 'Florida: MGT 462 '
    num_students = 0

    def __init__(self):
        print('Instantiated a DataPrep object')

    def prep_data_lms(self, input_data):
        def is_in_florida(ser):
            # filter only Florida data
            cond = \
                ser['Lesson'] == self.lesson and \
                ser['Lesson Completion'] == 'completed'
            if cond:
                return True
            else:
                return False

        self.read_inputs(input_data)
        ## START LMS DATA PROCESS
        self.lms_data = \
            self.lms_data.rename(columns=lambda x: x.strip())

        self.lms_data['FilteredInClass'] = self.lms_data.apply(
            is_in_florida, axis=1).astype(
            'bool')
        is_fil = self.lms_data['FilteredInClass'] == True
        ## Only select rows
        lms_fl = self.lms_data[is_fil]
        # Drop Josh's record and other test users/instructors
        lms_fl = lms_fl[lms_fl['Last Name'] != 'DeVincenzo']
        # TODO: Rewrite to be non-mutation
        self.num_students = lms_fl.shape[0]

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

        # print(lms_fl.columns)

        ## recode_by_regex –> String
        ## Takes in a string and replaces it with a recoded version,
        ## Only returns the acronym in parentheses...
        # helper function meant to be used in apply function...
        def recode_by_regex(input_data):
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

    def prep_data_eval(self, input_data):
        ## START EVAL PROCESS
        input_data = input_data.rename(columns=lambda x: x.strip())

        ## Filter columns by regular expressions
        df_only_questions = eval_df.filter(
            axis='columns',
            regex='Stu[0-9]+')

        df_only_likerts = df_only_questions.drop(
            labels=['Stu24', 'Stu25', 'Stu26', 'Stu27'], axis=1) \
            .fillna(0) \
            .astype(int)  # \
        # .recode()# TODO: Recode out-of-range-values to 0

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
            n=self.num_students,
            random_state=0)
        # TODO pass the random sample to be entered in

        print(len(df_rename_sampled))
        self.prepped_data_eval = df_rename_sampled
        return self.prepped_data_eval

    def prep_data_meta(self, input_meta):
        return self.prepped_data_meta

    def read_inputs(self, input_data_lms):
        self.lms_data = input_data_lms


# END OF CLASS
# Testing code below

out_data_test = DataPrep()
lms_path = 'data_in2/2019-07-18-12-32-33_d43o0sted3.csv'

# Import ZipGrade data...
eval_path = './data_in2/quiz-Eval-full.csv'
eval_df = pd.read_csv(eval_path, encoding='latin1')
A_final_lms = out_data_test.prep_data_lms(pd.read_csv(lms_path))
A_final_eval = out_data_test.prep_data_eval(eval_df)
A_final_meta = out_data_test.prep_data_eval(eval_df)

print(A_final_lms)
print(A_final_eval)
print(A_final_meta)