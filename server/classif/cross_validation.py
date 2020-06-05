from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score, KFold
from sklearn.metrics import roc_auc_score

from pyriemann.classification import MDM
from pyriemann.estimation import ERPCovariances, Covariances
import joblib

"""
This module provides buildin method for crossvalidation.
"""

def __get__proto__class__(class_name, class_info):
    return [class_info[class_name]]


"""
This method interpret a custom method passed as a string.
The parameters are fullfilled by the classification.py module and always respects this order:
- args[0] = X
- args[1] = Y
- args[2] = class_name
- args[3] = class_info
Except for vr dataset (see 'erp_cov_vr_pc' bellow):
- args[0] = X_training
- args[1] = labels_training
- args[2] = X_test
- args[3] = labels_test
- args[4] = class_name
- args[5] = class_info
"""
def custom(*args):
    local_variables = {'args': args}
    exec(args[-1], globals(), local_variables)
    return local_variables['ret']


def erp_cov(X, y, class_name, class_info):
    c = __get__proto__class__(class_name, class_info)
    skf = StratifiedKFold(n_splits=5)
    clf = make_pipeline(ERPCovariances(estimator='lwf', classes=c), MDM())
    return cross_val_score(clf, X, y, cv=skf, scoring='roc_auc').mean()


def cov(X, y, class_name, class_info):
    skf = StratifiedKFold(n_splits=5)
    clf = make_pipeline(Covariances(estimator='lwf'), MDM())
    return cross_val_score(clf, X, y, cv=skf).mean()


def erp_cov_vr_pc(X_training, labels_training, X_test, labels_test, class_name, class_info):
    # estimate the extended ERP covariance matrices with Xdawn
    erpc = ERPCovariances(classes=[class_info[class_name]], estimator='lwf')
    erpc.fit(X_training, labels_training)
    covs_training = erpc.transform(X_training)
    covs_test = erpc.transform(X_test)

    # get the AUC for the classification
    clf = MDM()
    clf.fit(covs_training, labels_training)
    labels_pred = clf.predict(covs_test)
    return roc_auc_score(labels_test, labels_pred)
