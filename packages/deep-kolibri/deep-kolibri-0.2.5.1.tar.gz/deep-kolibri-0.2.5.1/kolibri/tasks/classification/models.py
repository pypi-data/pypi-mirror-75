# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:

import numpy as np
import sklearn.svm as svm
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn_crfsuite import CRF
from xgboost import XGBClassifier

n_estimators = 10


def get_model(model_type):
    return {
        'logreg': LogisticRegression(random_state=0, multi_class='auto'),
        'logreg_l2': LogisticRegression(penalty='l2', tol=0.0001, C=1.0),
        'logreg_l1': LogisticRegression(penalty='l1', tol=0.0001, C=1.0),

        'svm': OneVsRestClassifier(
            BaggingClassifier(svm.SVC(kernel="linear", probability=True), max_samples=1.0 / n_estimators,
                              n_estimators=n_estimators)),
        'knn': KNeighborsClassifier(
            n_neighbors=10,
            algorithm='brute',
            metric='cosine',
            n_jobs=2),
        'nb-multinomial': MultinomialNB(),
        'mlp': MLPClassifier(),
        'rf': RandomForestClassifier(max_depth=20, random_state=50, n_jobs=-1),
        'dt': DecisionTreeClassifier(
            random_state=789654,
            criterion="gini"),
        'xgb': XGBClassifier(
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.7,
            objective='multi:softmax',
            silent=True,
            booster='gbtree',
            learning_rate=0.05,
            n_jobs=-1),
        'linearsvm': CalibratedClassifierCV(svm.LinearSVC(dual=False)),
        'crf': CRF(
            algorithm='lbfgs',
            c1=1,
            c2=0.1,
            max_iterations=100,
            # include transitions that are possible, but not observed
            all_possible_transitions=True
        )
    }.get(model_type.lower(), None)


def get_online_model(model_type):
    return {
        'sgdclassifier': SGDClassifier(max_iter=5, loss='modified_huber'),
        'perceptron': Perceptron(),
        'nb-multinomial': MultinomialNB(alpha=0.01),
        'nb-bernoulli': BernoulliNB(alpha=0.01),
        'passive-aggressive': PassiveAggressiveClassifier(),
    }.get(model_type.lower(), None)


def get_model_with_parms(model_type, params):
    if model_type == "logistic_regression":
        model = LogisticRegression(params)
    elif model_type == "random_forest":
        model = RandomForestClassifier(params)
    elif model_type == "decision_tree":
        model = DecisionTreeClassifier(params)
    elif model_type == "knn":
        model = KNeighborsClassifier(params)
    elif model_type == "bayes":
        model = MultinomialNB(params)
    elif model_type == "xgboost":
        model = XGBClassifier(params)
    elif model_type == "svm":
        model = svm.SVC(params)
    elif model_type == 'mlp':
        model = MLPClassifier(params)

    return model


def get_model_parameters_range(model_type):
    paramgrid = {}
    if model_type == 'logistic_regression':
        paramgrid = {"penalty": ['l1', 'l2'],
                     "C": np.logspace(0, 4, 10)}
    elif model_type == 'svm':
        paramgrid = {"kernel": ["rbf", "linear"],
                     "C": np.logspace(-9, 9, num=25, base=10),
                     "gamma": np.logspace(-9, 9, num=25, base=10),
                     "probability": [True]}
    elif model_type == "decision_tree":
        paramgrid = {"criterion": ['gini', 'entropy'],
                     "min_samples": [2, 3, 4],
                     "class_weight": ['balanced', 'None']}
    elif model_type == "random_forest":
        paramgrid = {"n_estimators": [100, 200, 300, 400],
                     "max_features": ['auto', 'sqrt'],
                     "max_depth": np.linspace(10, 110, num=11),
                     "bootstrap": [True, False]
                     }
    elif model_type == "knn":
        paramgrid = {"n_neighbors": [4, 5, 6, 7, 8, 9, 10],
                     "algorithm": ['auto', 'ball_tree', 'kd_tree', 'brute'],
                     "p": [1, 2],
                     "weights": ['uniform', 'distance']}
    elif model_type == 'bayes':
        paramgrid = {"alpha": np.logspace(0, 2, 10),
                     "fit_prior": [True, False]}

    elif model_type == "xgboost":
        paramgrid = {'booster': ['gbtree', 'gblinear'], 'learning_rate': np.logspace(0.01, 0.5, 10),
                     'max_depth': [3, 4, 5, 6, 7, 8, 9, 10], 'gamma': np.logspace(0, 2, 10)}
    elif model_type == 'mlp':
        paramgrid = {'solver': ['lbfgs'], 'max_iter': [500, 1000, 1500], 'alpha': 10.0 ** -np.arange(1, 7),
                     'hidden_layer_sizes': np.arange(5, 12)}

    return paramgrid
