from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score, KFold
from sklearn.externals import joblib
from sklearn.metrics import roc_auc_score

from pyriemann.classification import MDM
from pyriemann.estimation import ERPCovariances, Covariances


def __get__proto__class__(class_name, class_info):
    for k, v in class_info.items():
        if(not k == class_name):
            return [v]


def erp_cov(X, y, class_name, class_info):
    c = __get__proto__class__(class_name, class_info)
    skf = StratifiedKFold(n_splits=5)
    clf = make_pipeline(ERPCovariances(estimator='lwf', classes=c), MDM())
    return cross_val_score(clf, X, y, cv=skf, scoring='roc_auc').mean()


def cov(X, y, class_name, class_info):
    skf = StratifiedKFold(n_splits=5)
    clf = make_pipeline(Covariances(estimator='lwf'), MDM())
    return cross_val_score(clf, X, y, cv=skf).mean()


def erp_cov_vr_pc(X_training, labels_training, X_test, labels_test, ClassName, ClassInfo):
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
