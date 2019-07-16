import pandas as pd

lms_path = "data_original/2019-07-16-11-01-11_u0apmv5n7p.csv"
eval_path = "data_original/quiz-Eval-full (1).csv"

lms_data = pd.read_csv(lms_path)
evaldata = pd.read_csv(eval_path)
list(lms_data)
var = evaldata.describe

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
def buildRegistrationXML(df):
    df.apply(
        lambda row: # this lambda function is used to build 1 single XML node...
        print(
            row['First Name'], row['Last Name']
        ),
        axis=1)
    # for row in df.iteruples(index=)
    # currentRow =  #get current row and pass into a function?
    # functions in python don't have to return


buildRegistrationXML(lms_fl_subset.head(1))

exit()
