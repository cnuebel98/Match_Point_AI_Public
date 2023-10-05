from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

kFold_val = 3
scaler = StandardScaler() # MinMaxScaler() #MaxAbsScaler()
models = {
    'DT': DecisionTreeClassifier(),
    'GradBoost': GradientBoostingClassifier(),
    'bagging': BaggingClassifier(),
    'KNN': KNeighborsClassifier(),
    'GNB': GaussianNB(),
    'SVM': SVC(),
    'LogReg': LogisticRegression(),
    'SGD': SGDClassifier(),
    'LinSVC': LinearSVC(),
    'RF': RandomForestClassifier()
}

models_test = {
    'DT': DecisionTreeClassifier(),
}

# Set to False when only testing the dataset for errors
hyperparameter_tuning = True
hyperparameter_search = {

'RF' : {"max_depth": [5,10,15],
                  "n_estimators":[5,10,15,20],
                     "max_features": ['auto', 'sqrt','log2'],
                     "min_samples_split": [3, 10],
                     "min_samples_leaf": [3, 10],
                     "bootstrap": [True, False],
                     "criterion": ["gini", "entropy"]},

'DT' : {'criterion': ["entropy", "gini"],
      'max_depth': [5, 10, 15, 25, 30, 35, 40],
      'min_samples_split': [2, 5],
      'min_samples_leaf': [1, 2],
      'max_features': [1, 2]},

'GradBoost' : {'learning_rate':[0.15, 0.1, 0.10],
           'n_estimators': [10,20,30],
           'max_depth':[5,10,15],
           'min_samples_split':[5,10,15],
           'max_features':list(range(7,15))},

'bagging': {'n_estimators': [10, 20, 30, 40],
            'max_samples': [2, 5, 10, 15, 20],
            'max_features': [1, 2, 5, 10]},

'KNN': {'leaf_size': list(range(1, 50)),
        'n_neighbors': list(range(1, 30)),
        'p': [1, 2]},

'SVM': {'C': [0.1, 1, 10, 100],
        'kernel': ['rbf', 'poly', 'sigmoid', 'linear'],
        'degree': [1, 2, 3, 4]},

'GNB': {'priors': [None],
        'var_smoothing': [0.00000001, 0.000000001, 0.00000001]},

'LogReg': {'penalty': ['none', 'l1', 'l2', 'elasticnet'],
           'class_weight': ['balanced', 'None'],
           'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']},

'SGD': {'alpha': [1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3],  # learning rate
        'n_iter_no_change': [10, 100],  # number of epochs
        'loss': ['hinge', 'log', 'modified_huber', 'squared_hinge', 'huber'],
        'penalty': ['l2', 'l1', 'elasticnet'],
        'n_jobs': [-1, 1, 'None']},

'LinSVC': {
    'multi_class': ['ovr', 'crammer_singer'],
    'loss': ['log', 'squared_hinge'],
    'penalty': ['l2', 'l1'],
    'class_weight': ['dict', 'balanced']}
}