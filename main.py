# import sys

# path = __file__[0:-8] + '/py.BI.EEG.2012-GIPSA/brainInvaders2012/'
# sys.path.append(path)
# path = __file__[0:-8] + '/py.BI.EEG.2012-GIPSA/'
# sys.path.append(path)

from braininvaders2012.dataset import BrainInvaders2012
from braininvaders2013.dataset import BrainInvaders2013
from braininvaders2014a.dataset import BrainInvaders2014a
from braininvaders2014b.dataset import BrainInvaders2014b
from braininvaders2015a.dataset import BrainInvaders2015a
from braininvaders2015b.dataset import BrainInvaders2015b
from alphawaves.dataset import AlphaWaves
from headmounted.dataset import HeadMountedDisplay
from virtualreality.dataset import VirtualReality
from virtualreality.utilities import get_block_repetition
from moabb.paradigms import P300

from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score, KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib
from sklearn.metrics import roc_auc_score

from pyriemann.classification import MDM
from pyriemann.estimation import ERPCovariances, Covariances
from tqdm import tqdm
import numpy as np
import mne
import pandas as pd
from Parameters import Parameters, getDefaultBi2015a, getDefaultBi2015b, getDefaultAlpha
from Store import Store

import warnings
warnings.filterwarnings("ignore")

# filter data and resample


def baseFilter(raw, minF, maxF, sfResample=None):
    raw.filter(minF, maxF, verbose=False)
    if(not sfResample == None):
        raw.resample(sfResample, verbose=False)

# detect the events and cut the signal into epochs


def epoching(raw, Class1Value, Class2Value, tmin, tmax, Class1Name='NonTarget', Class2Name='Target'):
    events = mne.find_events(raw=raw, shortest_event=1, verbose=False)
    event_id = {Class1Name: Class1Value, Class2Name: Class2Value}
    epochs = mne.Epochs(raw, events, event_id, tmin=tmin,
                        tmax=tmax, baseline=None, verbose=False, preload=True)
    epochs.pick_types(eeg=True)
    return (events, epochs, event_id)

# cross validation


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


def getData(dataset, subject):
    return dataset._get_single_subject_data(subject)


def getBaseTrialAndLabel(epochs, events, fixIndex=False):
    y = events[:, -1]
    return epochs.get_data(), y - 1 if fixIndex else y


def useStore(params, store, key, validationMethod, *args):
    if params.useCache:
        if key in store:
            ret = store[key]
        else:
            ret = validationMethod(*args)
            store[key] = ret
    else:
        ret = validationMethod(*args)
    return ret


def classify2012(dataset, params, store):
    scr = {}

    for lz in params.getBi2012(dataset):

        print('running', lz)

        data = getData(dataset, lz.subject)
        raw = data['session_1']['run_training']

        baseFilter(raw, lz.fMin, lz.fMax, lz.resampling)
        events, epochs, _ = epoching(
            raw, 1, 2, lz.tmin, lz.tmax)

        # get trials and labels
        X, y = getBaseTrialAndLabel(epochs, events)
        y = LabelEncoder().fit_transform(y)

        ret = useStore(params, store, lz, crossValidationERP,
                       X, y, lz.condition)

        scr[str(lz)] = ret

    return scr


def classify2013(dataset, params, store):
    scores = {}

    # get the data from subject of interest
    for lz in params.getBi2013(dataset):

        print('running', lz)

        data = getData(dataset, lz.subject)

        raw = data[lz.session]['run_3']

        baseFilter(raw, lz.fMin, lz.fMax, lz.resampling)

        events, epochs, _ = epoching(raw, 33286, 33285, lz.tmin, lz.tmax)

        # get trials and labels
        X, y = getBaseTrialAndLabel(epochs, events)
        y[y == 33286] = 0
        y[y == 33285] = 1

        scores[str(lz)] = useStore(params, store, lz, crossValidationERP,
                                   X, y, lz.condition)

    return scores


def classify2014a(dataset, params, store):
    scr = {}

    for lz in params.getBi2014a(dataset):

        # load data
        print('running subject', lz)
        sessions = getData(dataset, lz.subject)
        raw = sessions['session_1']['run_1']

        baseFilter(raw, lz.fMin, lz.fMax)
        events, epochs, _ = epoching(raw, 1, 2, lz.tmin, lz.tmax)

        # get trials and labels
        X, y = getBaseTrialAndLabel(epochs, events, fixIndex=True)

        scr[str(lz)] = useStore(params, store, lz, crossValidationERP,
                                X, y, lz.condition)

    return scr


def classify2014b(dataset, params, store):
    scores = {}

    for lz in params.getBi2014b(dataset):

        print('running pair', lz)

        sessions = dataset._get_single_pair_data(pair=lz.pair)

        if lz.xpdesign == 'solo':
            raw = sessions['solo_' + str(lz.subject)]['run_1']
        else:
            raw = sessions['collaborative']['run_1']

        pick_channels = raw.ch_names[0 if lz.subject == 1 else 32:
                                     32 if lz.subject == 1 else -1] + [raw.ch_names[-1]]

        raw = raw.copy().pick_channels(pick_channels)

        baseFilter(raw, lz.fMin, lz.fMax, lz.resampling)
        events, epochs, _ = epoching(raw, 1, 2, lz.tmin, lz.tmax)

        # get trials and labels
        X, y = getBaseTrialAndLabel(epochs, events, fixIndex=True)

        scores[str(lz)] = useStore(params, store, lz, crossValidationERP,
                                   X, y, lz.condition)

    return scores


def classify2015a(dataset, params, store):
    scr = {}

    # note that subject 31 at session 3 has a few samples which are 'nan'
    # to avoid this problem it could be preferable to dropped the epochs having this condition

    for lz in params.getBi2015a(dataset):

        print('running', lz)
        sessions = getData(dataset, lz.subject)

        raw = sessions[lz.session]['run_1']

        baseFilter(raw, lz.fMin, lz.fMax, lz.resampling)

        events, epochs, _ = epoching(raw, 1, 2, lz.tmin, lz.tmax)

        # get trials and labels
        X, y = getBaseTrialAndLabel(epochs, events, fixIndex=True)

        scr[str(lz)] = useStore(params, store, lz, crossValidationERP,
                                X, y, lz.condition)

    return scr


def classify2015b(dataset, params, store):
    scores = {}

    for lz in params.getBi2015b(dataset):

        print('running', str(lz))

        sessions = dataset._get_single_pair_data(pair=lz.pair)

        raw = sessions[lz.session]['run_1']

        pick_channels = raw.ch_names[0 if lz.subject == 1 else 32:
                                     32 if lz.subject == 1 else -1] + [raw.ch_names[-1]]

        raw = raw.copy().pick_channels(pick_channels)

        baseFilter(raw, lz.fMin, lz.fMax, lz.resampling)

        events, epochs, _ = epoching(raw, 1, 2, lz.tmin, lz.tmax)

        # get trials and labels
        X, y = getBaseTrialAndLabel(epochs, events, fixIndex=True)
        y = epochs.events[:, -1]
        y = y - 1
        scores[str(lz)] = useStore(params, store, lz, crossValidationERP,
                                   X, y, lz.condition)

    return scores


def classifyAlphaWaves(dataset, params, store):
    scr = {}
    for lz in params.getAlpha(dataset):
        print('running', lz)
        raw = getData(dataset, lz.subject)

        baseFilter(raw, lz.fMin, lz.fMax, lz.resampling)

        conditions = {'closed': 1, 'open': 2}
        events, epochs, _ = epoching(
            raw, conditions['closed'], conditions['open'], lz.tmin, lz.tmax, 'closed', 'open')

        # get trials and labels
        X, y = getBaseTrialAndLabel(epochs, events)

        scr[str(lz)] = useStore(params, store, lz, crossValidation,
                                X, y, lz.condition, conditions)

    return scr


def classifyVR(dataset):
    # get the paradigm
    paradigm = P300()

    # loop to get scores for each subject
    nsubjects = 1

    df = {}
    for tmax in [0.2, 0.3]:
        print('tmax', tmax)
        paradigm.tmax = tmax

        scores = []
        for subject in dataset.subject_list[:nsubjects]:
            print('subject', subject)

            scores_subject = [subject]
            for condition in ['VR', 'PC']:
                print('condition', condition)

                # define the dataset instance
                dataset.VR = True if condition is 'VR' else False
                dataset.PC = True if condition is 'PC' else False

                # get the epochs and labels
                X, labels, meta = paradigm.get_data(
                    dataset, subjects=[subject])
                labels = LabelEncoder().fit_transform(labels)

                kf = KFold(n_splits=6)
                repetitions = [1, 2]
                auc = []

                blocks = np.arange(1, 13)
                for train_idx, test_idx in kf.split(np.arange(12)):

                    # split in training and testing blocks
                    X_training, labels_training, _ = get_block_repetition(
                        X, labels, meta, blocks[train_idx], repetitions)
                    X_test, labels_test, _ = get_block_repetition(
                        X, labels, meta, blocks[test_idx], repetitions)

                    val = crossValidationVR(
                        X_training, labels_training, X_test, labels_test)
                    auc.append(val)

                # stock scores
                scores_subject.append(np.mean(auc))

            scores.append(scores_subject)

        # print results
        df[tmax] = pd.DataFrame(scores, columns=['subject', 'VR', 'PC'])

    return df


def classifyPHMDML(dataset):

    scr = {}
    subject = 1
    for subject in [1]:

        print('subject', subject)
        # get the raw object with signals from the subject (data will be downloaded if necessary)
        raw = getData(dataset, subject)
        baseFilter(raw, 1, 35, 128)

        dict_channels = {chn: chi for chi, chn in enumerate(raw.ch_names)}

        # cut the signals into epochs and get the labels associated to each trial
        events, epochs, event_id = epoching(raw, 1, 2, 10, 50, 'OFF', 'ON')

        X = epochs.get_data()
        inv_events = {k: v for v, k in event_id.items()}
        labels = np.array([inv_events[e] for e in epochs.events[:, -1]])

        scr[subject] = crossValidation(X, labels)

    return scr


store = Store()

args = getDefaultAlpha()
args['subject'] = [1]
params = Parameters(True, **args)

# dataset_2012 = BrainInvaders2012(Training=True)
# scr = classify2012(dataset_2012, params, store)

# dataset_2013 = BrainInvaders2013(
#     NonAdaptive=True, Adaptive=False, Training=True, Online=False)
# scr = classify2013(dataset_2013, params, store)

# dataset_2014a = BrainInvaders2014a()
# scr = classify2014a(dataset_2014a, params, store)

# dataset_2014b = BrainInvaders2014b()
# scr = classify2014b(dataset_2014b, params, store)

# dataset_2015a = BrainInvaders2015a()
# scr = classify2015a(dataset_2015a, params, store)

# dataset_2015b = BrainInvaders2015b()
# scr = classify2015b(dataset_2015b, params, store)

dataset_alphaWaves = AlphaWaves(useMontagePosition=False)
scr = classifyAlphaWaves(dataset_alphaWaves, params, store)

# dataset_VR = VirtualReality(useMontagePosition=False)
# scr = classifyVR(dataset_VR)

# dataset_PHMDML = HeadMountedDisplay(useMontagePosition=False)
# scr = classifyPHMDML(dataset_PHMDML)

store.save()

print(scr)
