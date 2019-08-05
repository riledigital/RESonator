import pandas as pd
import xml.etree.ElementTree as ET
import re
import datetime

from sys import exit
import xml.dom as DOM

# TODO: make file pickers for selecting CSV files

# GET ALL INPUT FILES
dir_in = 'data_in2'
dir_out = 'data_out'
lms_path = 'data_in2/2019-07-18-12-32-33_d43o0sted3.csv'
lms_data = pd.read_csv(
    lms_path)
lms_data = lms_data.rename(
    columns=lambda x: x.strip())
# Remove whitespace from column names, end and beginning
# lms_data[''] = lms_data[]

# print(list(lms_data))

lesson = 'Florida: MGT 462 '

# TODO: clean up lesson codes...
# TODO: replace trailing spaces
# TODO: replace
# TODO: strip all whitespace from column values with strings?

def is_filtered(ser):
    # filter only Florida data
    cond = ser['Lesson'] == lesson and \
           ser['Lesson Completion'] == 'completed'
    if cond:
        return True
    else:
        return False

lms_data['FilteredInClass'] = lms_data.apply(
    is_filtered, axis=1).astype('bool')  # Create a new field for Filtered...
is_fil = lms_data['FilteredInClass'] == True  ## Only select rows
lms_fl = lms_data[is_fil]
# Drop Josh's record and other test users/instructors
lms_fl = lms_fl[lms_fl['Last Name'] != 'DeVincenzo']

# TODO: Rewrite to be non-mutation
num_students = lms_fl.shape[0]

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
def recode_acronyns_parens(input_data):
    regex_str = '\([A-Z]+\)'
    regex = re.compile(regex_str)
    # p = re.compile(regex_str)  # parentheses for capture groups
    sr = re.search(pattern=regex, string=input_data)
    captured = sr.group().strip('()')  # remove the parentheses
    return captured

# Recode values for fields
lms_fl_subset['Government Level'] = \
    lms_fl_subset['Government Level'].apply(recode_acronyns_parens)
lms_fl_subset['Discipline'] = \
    lms_fl_subset['Discipline'].apply(recode_acronyns_parens)

# Export a CSV of filtered LMS
# lms_fl_subset.to_csv('data_out/lms_fl_subsetted.csv')

# Build the node for registration which will be appended later...
registration = ET.Element('registration')  # initialize XML node

# row_to_xml
# row: Series representing user data
# this helper function creates a new XML node
# for students, using the selected fields.
# returns: returns null.
def row_to_xml(row):
    new_student = ET.Element('student', attrib={
        'international': row['International Status'],
        'studentfirstname': row['First Name'],
        'studentlastname': row['Last Name'],
        'studentcity': row['City'],
        'studentzipcode': row['Postal Code'],
        'studentphone': row['Primary Phone'],
        'discipline': row['Discipline'],
        'govnlevel': row['Government Level']})
    registration.append(new_student)
    # print("Appended record: " + str(row['First Name']))


# This function outputs nothing
# build_registration_xml
# df: data frame representing user data from LMS system
def build_registration_xml(df):
    df.apply(row_to_xml, axis=1)


build_registration_xml(lms_fl_subset)
registration_tree = ET.ElementTree(registration)
# registration_tree.write('data_out/test.xml')

# Next...
# Import ZipGrade data...
eval_path = './data_in2/quiz-Eval-full.csv'
eval_df = pd.read_csv(eval_path, encoding='latin1')
eval_df = eval_df.rename(columns=lambda x: x.strip())
evaldata = ET.Element(
    'evaldata')  # initialize XML node representing set of all evaluations

# df_identifiers = eval_df.filter(  # Filter only the columns we want
#     axis='columns',
#     items=['StudentID'])

df_only_questions = eval_df.filter(  ## Filter columns by regular expressions
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

## If the ZipGrade input does not have empty fields for Stu23 to Stu27,
## Just make empty ones...
# df_ready = df_cleaned.assign(  # Create empty fields for written questions...
#     id24='',
#     id25='',
#     id26='',
#     id27='')

#  Rename column names to replace Stu with id
df_rename = df_merged_responses
df_rename.columns = [
    col.replace('Stu', 'id') for col in df_rename.columns]
df_rename_sampled = df_rename.sample(
    n=num_students,
    random_state=0)  # TODO pass the random sample to be entered in

print(len(df_rename_sampled))