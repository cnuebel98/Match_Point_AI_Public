import pandas as pd
import scipy.stats
import config2
from train_functionals_2 import *


df = pd.read_csv(r'C:\Users\carlo\TrainingsTool\Tennis\ML_Stuff\first_serve_djoko_dir_v1.csv', encoding='unicode_escape', low_memory=False)

target = '0_dir'

dataframe_result = pd.DataFrame(columns=['model_name',

                                         "acc_train", "b_acc_train", "pre_train", "rec_train", "fscore_train",
                                         "acc_val", "b_acc_val", "pre_val", "rec_val", "fscore_val",
                                         "acc_test", "b_acc_test", "pre_test", "rec_test", "fscore_test",

                                         'target'])


for model_name, model in config2.models.items():
    # apply scaler to df without target
    #df_scaled = config2.scaler.fit_transform(df.drop(target, axis=1))
    # to keep columname since scale strips column name
    #df_scaled_no_target = pd.DataFrame(df_scaled, columns=df.drop(target, axis=1).columns)

    # add target to df
    #df_scaled_no_target[target] = df[target]  # df_train[target]
    # element[0]['thi_score']

    result_f = result(df.copy(), model, model_name, target=target)
    dataframe_result.loc[len(dataframe_result)] = result_f
    print(model_name)

dataframe_result.to_csv('results.csv', sep=';', decimal=',', index=False)