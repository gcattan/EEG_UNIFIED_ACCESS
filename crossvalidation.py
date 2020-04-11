from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score, KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib
from sklearn.metrics import roc_auc_score

from pyriemann.classification import MDM
from pyriemann.estimation import ERPCovariances, Covariances


def crossValidationERP(X, y, ClassName='Target', ClassInfo={'Target': 1, 'NonTarget': 2}):
    skf = StratifiedKFold(n_splits=5)
    clf = make_pipeline(ERPCovariances(estimator='lwf', classes=[
                        ClassInfo[ClassName]]), MDM())
    return cross_val_score(clf, X, y, cv=skf, scoring='roc_auc').mean()


def crossValidation(X, y, ClassName='Target', ClassInfo={'Target': 1, 'NonTarget': 2}):
    skf = StratifiedKFold(n_splits=5)
    clf = make_pipeline(Covariances(estimator='lwf'), MDM())
    return cross_val_score(clf, X, y, cv=skf).mean()


def crossValidationVR(X_training, labels_training, X_test, labels_test, ClassName='Target', ClassInfo={'Target': 1, 'NonTarget': 0}):
    # estimate the extended ERP covariance matrices with Xdawn
    # dict_labels = {'Target':1, 'NonTarget':0}
    erpc = ERPCovariances(classes=[ClassInfo[ClassName]], estimator='lwf')
    erpc.fit(X_training, labels_training)
    covs_training = erpc.transform(X_training)
    covs_test = erpc.transform(X_test)

    # get the AUC for the classification
    clf = MDM()
    clf.fit(covs_training, labels_training)
    labels_pred = clf.predict(covs_test)
    return roc_auc_score(labels_test, labels_pred)
