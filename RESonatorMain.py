import pandas as pd
import DataPrep as dp
import XMLGenerator as xmlgen

lms_path = './data_in2/2019-07-18-12-32-33_d43o0sted3.csv'
path_eval = './data_in2/quiz-Eval-full.csv'
path_meta = './data_in2/meta-template.csv'

lms_df = pd.read_csv(lms_path, encoding='latin1')
eval_df = pd.read_csv(path_eval, encoding='latin1')
meta_df = pd.read_csv(path_meta, encoding='latin1')
lesson_str = 'Florida: MGT 462 '

out_data_test = dp.DataPrep(lms_df, eval_df, meta_df)
A_final_lms = out_data_test.prep_data_lms()
A_final_eval = out_data_test.prep_data_eval()
A_final_meta = out_data_test.prep_data_meta()

generator = xmlgen.XMLGenerator(A_final_lms, A_final_eval, A_final_meta)
generator.generate_xml()
