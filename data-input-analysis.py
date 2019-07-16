import pandas as pd
import xml.etree.ElementTree as ET

lms_path = "data_original/2019-07-16-11-01-11_u0apmv5n7p.csv"
eval_path = "data_original/quiz-Eval-full (1).csv"

lms_data = pd.read_csv(lms_path)
eval_data = pd.read_csv(eval_path)
list(lms_data)
var = eval_data.describe

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


# build registration
# df: dataframe from LMS representing a student
roster = ET.Element('registration')  # initialize XML node


# this helper function creates 1 row.
def row_to_xml(row):
    new_student = ET.Element('student')
    new_student.set('international', row['International Status '])
    new_student.set('studentfirstname', row['First Name'])
    new_student.set('studentlastname', row['Last Name'])
    new_student.set('studentcity', row['City'])
    new_student.set('studentzipcode', row['Postal Code'])
    new_student.set('studentphone', row['Primary Phone'])
    new_student.set('discipline', row['Discipline '])
    roster.append(new_student)
    print("Appended record: " + str(row['First Name']))


def build_registration_xml(df):
    df.apply(row_to_xml, axis=1)


build_registration_xml(lms_fl_subset)
tree = ET.ElementTree(roster)
tree.write('data_out/test.xml')
exit()