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
from Parameters import Parameters
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


def crossValidationERP(X, y, ClassName='Target', ClassInfo={'Target': 1, 'NonTarget': 2},):
    skf = StratifiedKFold(n_splits=5)
    clf = make_pipeline(ERPCovariances(estimator='lwf', classes=[
                        ClassInfo[ClassName]]), MDM())  # TODO Fix classes=[1]
    return cross_val_score(clf, X, y, cv=skf, scoring='roc_auc').mean()


def crossValidation(X, y):
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
    # get the data from subject of interest
    # for subject in dataset.subject_list:

    # Target|NonTarget
    # tmin|tmax
    # fMin|fMax
    # resampling
    # subject

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

        # if params.useCache:
        #     if lz in store:
        #         ret = store[lz]
        #     else:
        #         ret = crossValidationERP(
        #             X, y, lz.condition)
        #         store[lz] = ret
        # else:
        #     ret = crossValidationERP(
        #         X, y, lz.condition)

        ret = useStore(params, store, lz, crossValidationERP,
                       X, y, lz.condition)

        scr[str(lz)] = ret

    return scr


def classify2013(dataset):
    scores = {}

    # get the data from subject of interest
    for subject in [8]:

        print('running subject', subject)

        scores[subject] = {}

        data = getData(dataset, subject)

        for session in data.keys():

            print('running session', session)

            raw = data[session]['run_3']

            baseFilter(raw, 1, 24)

            events, epochs = epoching(raw, 33286, 33285, 0.0, 0.1)

            # get trials and labels
            X, y = getBaseTrialAndLabel(epochs, events)
            y[y == 33286] = 0
            y[y == 33285] = 1

            scr = crossValidationERP(X, y)

            scores[subject][session] = scr.mean()

    return scores


def classify2014a(dataset):
    scr = {}
    for subject in [1]:

        # load data
        print('running subject', subject)
        sessions = getData(dataset, subject)
        raw = sessions['session_1']['run_1']

        baseFilter(raw, 1, 20)
        events, epochs = epoching(raw, 1, 2, 0.0, 0.8)

        # get trials and labels
        X, y = getBaseTrialAndLabel(epochs, events, fixIndex=True)

        scr[subject] = crossValidationERP(X, y)

    return scr


def classify2014b(dataset):
    scores = {}

    for pair in [1]:
        scores[pair] = {}

        print('pair', str(pair))

        sessions = dataset._get_single_pair_data(pair=pair)

        for subject in [1, 2]:
            scores[pair][subject] = {}

            print('subject', subject)

            # subject 1
            raw_solo = sessions['solo_' + str(subject)]['run_1']
            if subject == 1:
                pick_channels = raw_solo.ch_names[0:32] + \
                    [raw_solo.ch_names[-1]]
            elif subject == 2:
                pick_channels = raw_solo.ch_names[32:-
                                                  1] + [raw_solo.ch_names[-1]]
            raw_solo.pick_channels(pick_channels)
            raw_cola = sessions['collaborative']['run_1']
            raw_cola = raw_cola.copy().pick_channels(pick_channels)

            for condition, raw in zip(['solo', 'cola'], [raw_solo, raw_cola]):

                baseFilter(raw, 0, 20)
                events, epochs = epoching(raw, 1, 2, 0.0, 0.8)

                # get trials and labels
                X, y = getBaseTrialAndLabel(epochs, events, fixIndex=True)

                scores[pair][subject][condition] = crossValidationERP(X, y)

    return scores


def classify2015a(dataset):
    scr = {}

    # note that subject 31 at session 3 has a few samples which are 'nan'
    # to avoid this problem it could be preferable to dropped the epochs having this condition

    # load data
    for subject in [1]:

        print('running subject', subject)
        sessions = getData(dataset, subject)
        scr[subject] = {}

        for session in sessions.keys():

            print('session', session)
            raw = sessions[session]['run_1']

            baseFilter(raw, 1, 24)

            events, epochs = epoching(raw, 1, 2, 0.0, 0.8)

            # get trials and labels
            X, y = getBaseTrialAndLabel(epochs, events, fixIndex=True)

            scr[subject][session] = crossValidationERP(X, y)

    return scr


def classify2015b(dataset):
    scores = {}
    for pair in [1]:
        scores[pair] = {}

        print('pair', str(pair))

        sessions = dataset._get_single_pair_data(pair=pair)
        for session_name in sessions.keys():

            print('session', session_name)
            scores[pair][session_name] = {}

            raw = sessions[session_name]['run_1']

            for subject in [1, 2]:

                if subject == 1:
                    pick_channels = raw.ch_names[0:32] + [raw.ch_names[-1]]
                elif subject == 2:
                    pick_channels = raw.ch_names[32:-1] + [raw.ch_names[-1]]

                raw_subject = raw.copy().pick_channels(pick_channels)

                baseFilter(raw, 1, 20)

                events, epochs = epoching(raw, 1, 2, 0.0, 0.8)

                # get trials and labels
                X, y = getBaseTrialAndLabel(epochs, events, fixIndex=True)

                scores[pair][session_name][subject] = crossValidationERP(X, y)

    return scores


def classifyAlphaWaves(dataset):
    scr = {}
    for subject in dataset.subject_list[0:2]:
        print('subject', subject)
        raw = getData(dataset, subject)

        baseFilter(raw, 3, 40, 128)

        events, epochs = epoching(raw, 1, 2, 2.0, 8.0, 'closed', 'open')

        # get trials and labels
        X, y = getBaseTrialAndLabel(epochs, events)

        scr[subject] = crossValidation(X, y)

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
params = Parameters(True, condition=['Target'], tmin=[0],
                    tmax=[1.0], resampling=[128], subject="30%", fMin=[1], fMax=[24])
# for lz in params.getBi2012():
#     print(lz.condition, lz.tmin, lz.tmax,
#           lz.resampling, lz.subject, lz.fMin, lz.fMax)

# load BrainInvaders instance


dataset_2012 = BrainInvaders2012(Training=True)
scr = classify2012(dataset_2012, params, store)

store.save()

# dataset_2013 = BrainInvaders2013(NonAdaptive=True, Adaptive=False, Training=True, Online=False)
# scr = classify2013(dataset_2013)

# dataset_2014a = BrainInvaders2014a()
# scr = classify2014a(dataset_2014a)

# dataset_2014b = BrainInvaders2014b()
# scr = classify2014b(dataset_2014b)

# dataset_2015a = BrainInvaders2015a()
# scr = classify2015a(dataset_2015a)

# dataset_2015b = BrainInvaders2015b()
# scr = classify2015b(dataset_2015b)

# dataset_alphaWaves = AlphaWaves(useMontagePosition=False)
# scr = classifyAlphaWaves(dataset_alphaWaves)

# dataset_VR = VirtualReality(useMontagePosition=False)
# scr = classifyVR(dataset_VR)

# dataset_PHMDML = HeadMountedDisplay(useMontagePosition=False)
# scr = classifyPHMDML(dataset_PHMDML)

print(scr)
