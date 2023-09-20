import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, train_test_split
from sklearn.model_selection import GridSearchCV
import config2
import os
import json
from sklearn.metrics import precision_recall_fscore_support, balanced_accuracy_score, accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import precision_score, recall_score, f1_score
from statistics import mean, stdev
import numpy as np



def get_best_hyper_per_fold(df, model, model_name, target):

    """
    this function take folowing params
    :param df: to run the model over it
    :param model: model to be trained
    :param model_name: model name to save it like in config
    :return: the best params of each models
    """
    #kf_test = KFold(n_splits=config.kFold_test, shuffle=True, random_state=42)
    kf_val = KFold(n_splits=config2.kFold_val, shuffle=True, random_state=42)

    hyper = []
    for train_index_outer, test_index_outer in kf_val.split(df):
        X = df.drop(target, axis=1).iloc[train_index_outer]
        #X = X[config2.input_cols]
        y = df[target].iloc[train_index_outer]

        # 20% of data not used for the hyperprams
        X_test = df.drop(target, axis=1).iloc[test_index_outer]
        y_test = df[target].iloc[test_index_outer]

        for train_index, val_index in kf_val.split(X):
            X_train, X_val = X.iloc[train_index], X.iloc[val_index]
            y_train, y_val = y.iloc[train_index], y.iloc[val_index]


            tuning = GridSearchCV(estimator=model,
                                  param_grid=config2.hyperparameter_search[model_name],
                                  scoring='balanced_accuracy', n_jobs=-1) #'neg_root_mean_squared_error'

            tuning.fit(X_val, y_val)
            tuning.best_params_, tuning.best_score_

            hyper.append(tuning.best_params_)
    return hyper

# --------------------- load the hyperparmas in json after tuning ---------------------------------------
def store_hyperparams(model_name, best_hyper):
    """
    this function save the frequent hyperparms of each model in json format
    :param model_name: model_name like it is config
    :param best_hyper: from the function best_hyper
    :param dataset: the dataset which is used for training
    :param thresh: this threshhold is used for different datasets
    :return: hyperparms in json
    """
    # create path
    folder_path ='results/hyperparams'
    #check if folder exists
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
    # else make folder

    #print('hyperparams is stored to: ', folder_path+'/'+model_name+'.json')
    with open(folder_path+'/'+model_name+'.json', 'w') as fp:
        json.dump(best_hyper, fp)


def load_hyperparams(model,data):
    """
    this function load the hyperparms for the model to be used directly after tuning
    :param model: the model to be run finaly
    :param data: the best params for the final run
    :return: the model with the best hyperprams
    """

   # Opening JSON file

    for k, v in data.items():
        setattr(model, k, v)
    return model



def most_common(lst):
    """
    this function take a list and return most frequent
    :param lst: list of hyperparams
    :return: the most frequent params
    """

    #TODO random explicty for 2 same frequent params
    return max(set(lst), key=lst.count)

def best_parameters(res_list):
    """
    this function take the most common params and save it in dict
    :param res_list: list with params
    :return: the best hyperparams with the name of them for the model as dict
    """
    #print('res_list = ', res_list)
    tmp_d = dict([(key, []) for key in res_list[0].keys()])

    for d in res_list:
        for k, v in d.items():
            tmp_d[k].append(v)
    tmp_d2 = {}
    for k in tmp_d.keys():
        tmp_d2[k] = most_common(tmp_d[k])
    #print('most_common = ', tmp_d2)
    return tmp_d2




def predict_and_store(clf,X,y,acc, b_acc, pre, rec, fscore):
    y_pred = clf.predict(X)
    acc.append(accuracy_score(y, y_pred))
    b_acc.append(balanced_accuracy_score(y, y_pred))
    pre.append(precision_score(y, y_pred, average='None'))
    rec.append(recall_score(y, y_pred, average='None'))
    fscore.append(f1_score(y, y_pred, average='None'))


    return acc,b_acc, pre, rec, fscore

def train_fist_it(df, model,model_name, target):
    """
    train the models
    :param df: got dataframe
    :param model: model (regression)
    :param model_name: name of them in config
    :return: the evaluation mertrics like RMSE and R^2 for each model on each datasets
    """

    #kf_test = KFold(n_splits=config.kFold_test, shuffle=True, random_state=42)
    #X_orginal = df.drop(target, axis=1)
    #y_orginal = df[target]

    #X, X_test, y, y_test = train_test_split(X_orginal,y_orginal, test_size=0.2, random_state=42, stratify=target)
    X = df.drop(target, axis=1)
    y = df[target]

    X, X_test, y, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    #X_orginal = df.drop(target, axis=1)
    #y_orginal = df[target]

    acc_train = []
    b_acc_train = []
    pre_train = []
    rec_train = []
    fscore_train = []

    acc_val = []
    b_acc_val = []
    pre_val = []
    rec_val = []
    fscore_val = []

    acc_test = []
    b_acc_test = []
    pre_test = []
    rec_test = []
    fscore_test = []




    #df_train_val = df.iloc[train_index_outer]

    # 20% of data not used for the hyperprams
    #X_test = df.drop(target, axis=1).iloc[test_index_outer]
    # X_test = X_test[config2.input_cols]
    #y_test = df[target].iloc[test_index_outer]



    kf_val = KFold(n_splits=config2.kFold_val, shuffle=True, random_state=42)

    for train_index, val_index in kf_val.split(X):
        X_train, X_val = X.iloc[train_index], X.iloc[val_index]
        y_train, y_val = y.iloc[train_index], y.iloc[val_index]

        '''
        X_train = X_train.drop(target, axis=1)
        X_val = X_val.drop(target, axis=1)
        y_train = y_train[target]
        y_val = y_val[target]
        '''
        clf = model
        clf.fit(X_train, y_train)

        acc_train,b_acc_train, pre_train, rec_train, fscore_train = predict_and_store(clf, X_train, y_train, acc_train, b_acc_train, pre_train, rec_train, fscore_train)

        acc_val,b_acc_val, pre_val, rec_val, fscore_val = predict_and_store(clf, X_val, y_val, acc_val,b_acc_val, pre_val, rec_val, fscore_val)

        acc_test,b_acc_test, pre_test, rec_test, fscore_test = predict_and_store(clf, X_test, y_test, acc_test,b_acc_test, pre_test, rec_test, fscore_test )


    #y_pred_test = clf.predict(X_test)
    #R_score_test = r2_score(y_test, y_pred_test)
    #RMSE_test = mean_squared_error(y_test, y_pred_test, squared=False)
        '''
          y_pred_test = clf.predict(X_test)
        cm = confusion_matrix(y_test, y_pred_test, labels=clf.classes_)
        # cm_l = np.array(cm_l)
        # cm = np.sum(cm_l, axis=0)
    
        # since we have inbalance classes use normalized cf
        cm = cm / cm.astype(np.float).sum(axis=1)[:, np.newaxis]
    
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
        disp.plot()
        plt.show()
        '''




    return [model_name,
            round(mean(acc_train), 4), round(mean(b_acc_train), 4),
            round(mean(pre_train), 4), round(mean(rec_train),4),
            round(mean(fscore_test), 4),

            round(mean(acc_val), 4), round(mean(b_acc_val), 4),
            round(mean(pre_val), 4), round(mean(rec_val), 4),
            round(mean(fscore_val), 4),

            round(mean(acc_test), 4), round(mean(b_acc_test), 4),
            round(mean(pre_test), 4), round(mean(rec_test), 4),
            round(mean(fscore_test), 4),

            target]



def result(df, model,model_name, target):
    """
    same like train but here item for subset of feature of the df
    :param df:
    :param model:
    :param model_name:
    :param item: each questainry here see config item_cols
    :param thresh:
    :return:
    """
    #dataframe_result = pd.DataFrame(
        #columns=['model_name', "RMSE_train_baseline", "RMSE_val_baseline", "RMSE_test_baseline",
                # "RMSE_train", "RMSE_val", "RMSE_test", 'R^2_train', 'R^2_val', 'R^2_test'])

    if config2.hyperparameter_tuning:

        #get best hyperparameters
        #returns list of best hyper parameters per fold
        hyper = get_best_hyper_per_fold(df, model,model_name, target)
        # get most common hyperparameters
        best_hyper = best_parameters(hyper)
        store_hyperparams(model_name, best_hyper)
        model = load_hyperparams(model,best_hyper)


    train_result= train_fist_it(df, model,model_name, target)




    return train_result









