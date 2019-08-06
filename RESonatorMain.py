import pandas as pd
import DataPrep as dp
import XMLGenerator as xmlgen

# END OF CLASS
# Testing code below

out_data_test = dp.DataPrep()
lms_path = 'data_in2/2019-07-18-12-32-33_d43o0sted3.csv'

# Import ZipGrade data...
eval_path = './data_in2/quiz-Eval-full.csv'
eval_df = pd.read_csv(eval_path, encoding='latin1')
meta_df = pd.read_csv('./data_in2/meta-template.csv')

A_final_lms = out_data_test.prep_data_lms(pd.read_csv(lms_path))
A_final_eval = out_data_test.prep_data_eval(eval_df)
A_final_meta = out_data_test.prep_data_meta(meta_df)

generator = xmlgen.XMLGenerator(A_final_lms, A_final_eval, A_final_meta)
generator.generate_xml()
