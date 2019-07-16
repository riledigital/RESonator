import pandas as pd
import xml.etree.ElementTree as ET

lms_path = "data_original/2019-07-16-11-01-11_u0apmv5n7p.csv"

lms_data = pd.read_csv(lms_path)
list(lms_data)

# filter only Florida data
selector = 'Florida: MGT 462 '
is_fl = lms_data['Lesson'] == selector
lms_fl = lms_data[is_fl]

# Get only the columns we need
lms_fl_subset = lms_fl.filter(
    items=[
        'Last Name',
        'First Name',
        'Job Title',
        'Street Address',
        'City',
        'State/Province',
        'Postal Code',
        'Primary Phone',
        'Email',
        'Discipline ',
        'Government Level ',
        'International Status '
        ## note that there are trailing whitespace
    ]
)

# Export a CSV of filtered LMS
lms_fl_subset.to_csv(
    'data_out/lms_fl_subsetted.csv'
)

# Build the node for registration which will be appended later...
registration = ET.Element('registration')  # initialize XML node


# row_to_xml
# row: Series representing user data
# this helper function creates a new XML node
# for students, using the selected fields.
# returns: returns null.
def row_to_xml(row):
    new_student = ET.Element('student')
    new_student.set('international', row['International Status '])
    new_student.set('studentfirstname', row['First Name'])
    new_student.set('studentlastname', row['Last Name'])
    new_student.set('studentcity', row['City'])
    new_student.set('studentzipcode', row['Postal Code'])
    new_student.set('studentphone', row['Primary Phone'])
    new_student.set('discipline', row['Discipline '])
    registration.append(new_student)
    print("Appended record: " + str(row['First Name']))


# This function outputs nothing
# build_registration_xml
# df: data frame representing user data from LMS system
def build_registration_xml(df):
    df.apply(row_to_xml, axis=1)


build_registration_xml(lms_fl_subset)
tree = ET.ElementTree(registration)
tree.write('data_out/test.xml')

# Next...
# Import ZipGrade data...
eval_path = "data_original/quiz-Eval-full (1).csv"
eval_df = pd.read_csv(eval_path)
current = eval_df.head(5)

# DONE: Subset only needed questions
# Get questions
# StuX
## eval_df_working = eval_df['StudentID']  # This can subset columns by labels if you know the names
df_identifiers = eval_df.filter(  # Filter only the columns we want
    axis='columns',
    items=['StudentID'],
)
df_only_questions = eval_df.filter(  ## Filter columns by regular expressions
    axis='columns',
    regex='Stu[0-9]+')

df_cleaned = df_identifiers.join(  # join one to another
    df_only_questions
)

df_ready = df_cleaned.assign(  # Create empty fields for written questions...
    id24='',
    id25='',
    id26='',
    id27=''
)

#  TODO: Create duplicate columns where question number can be identified?...
#  ex: question_index : int where 0-27

#  Rename column names to replace Stu with id
df_rename = df_ready
#  https://www.quora.com/How-can-I-replace-characters-in-a-multiple-column-name-in-pandas
df_rename.columns = [col.replace('Stu', 'id') for col in df_rename.columns]


# Pretest Avg,Posttest Avg,Course Name ,StudentID,QuizCreated,DataExported,id1,id2,id3,id4,id5,id6,id7,id8,id9,id10,id11,id12,id13,id14,id15,id16,id17,id18,id19,id20,id21,id22,id23,id24,id25,id26,id27

# TODO: ???? Rename question fields to "idX" where X is number of question??...
# TODO: Write helper function that takes in a row and creates an individual node
# TODO: Write function that takes in df, outputs an XML Element Tree

# make_eval_tree -> Element
# df: DataFrame representing evaluations
def make_eval_tree(df):
    df.apply(make_tree_from_question, axis=1)  # Apply function to all rows
    return evaldata


# TODO: move this variable declaration elsewhere...
evaldata = ET.Element('evaldata')  # initialize XML node representing set of all evaluations


# make_key_value
# series: A Series representing a column
# TODO: Helper function for creating a k-v pair ?
def make_key_value(series):
    # TODO: set attribs for each column in current question
    q_name = series.name  # TODO: get question name
    q_value = series.item  # TODO: question response value?...
    out.set(q_name, q_value)
    return {'key': 'value'}  # perhaps return a dict or array?...


# make_tree_from_question
# question: a Series representing a question...
def make_tree_from_question(question):
    out = ET.Element('question')
    question.apply(
        # TODO: write getter function
        make_key_value,
        axis=0  # only refer to columns
    )
    evaldata.append(out)


return evaldata  ## technically it shouldn't matter...

test_tree = make_eval_tree(df_rename)  # this test code uses the renamed eval data

test_tree_two = ET.ElementTree(test_tree)
test_tree_two.write('data_out/test-tree.xml')

# TODO: figure out how to fetch ID name for question
# TODO: Figure out how to fetch ID value  for question

# exit()
