import pandas as pd


# completed
# is_passed_class -> Boolean
# in: DF/series representing a class
# check if person passed the class
# TODO: Calculate the number of students who passed
def is_passed_class(inp):
    cond = inp.loc['Lesson Completion'] == 'completed' and \
           inp.loc['Lesson Success'] == 'passed'
    if cond:
        return True
    else:
        return False


lms_path = 'data_in2/2019-07-18-12-32-33_d43o0sted3.csv'
lms_data = pd.read_csv(lms_path)
lms_data = lms_data.rename(columns=lambda x: x.strip())  # Remove trailing and leading whitespace
lms_data['PassedClass'] = lms_data.apply(
    is_passed_class,
    axis=1).astype('bool')
list(lms_data)

# number of people who pass
print(lms_data['PassedClass'].describe())

# filter only Florida data
selector = 'Florida: MGT 462 '
is_fl = lms_data['Lesson'] == selector
lms_fl = lms_data[is_fl]

print(lms_fl['PassedClass'].describe())

criteria1 = ['completed', 'incomplete']
## TODO: Figure out a better way to filter the data...
## TODO: Consider cleaning up the field names
current_fl_test = lms_data.query('`Lesson Completion`.isin(criteria1)')

# TODO: create a function to calculate the number of students in the record... shouldn't be harder than
# length or size or w/e in R?...