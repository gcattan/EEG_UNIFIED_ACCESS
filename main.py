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

from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib
from pyriemann.classification import MDM
from pyriemann.estimation import ERPCovariances, Covariances
from tqdm import tqdm
import numpy as np
import mne

import warnings
warnings.filterwarnings("ignore")

# filter data and resample
def baseFilter(raw, minF, maxF):
    raw.filter(minF, maxF, verbose=False)

# detect the events and cut the signal into epochs
def epoching(raw, Class1Value, Class2Value, tmin, tmax, Class1Name = 'NonTarget', Class2Name = 'Target'):
    events = mne.find_events(raw=raw, shortest_event=1, verbose=False)
    event_id = {Class1Name: Class1Value, Class2Name : Class2Value}
    epochs = mne.Epochs(raw, events, event_id, tmin=tmin, tmax=tmax, baseline=None, verbose=False, preload=True)
    epochs.pick_types(eeg=True)
    return (events, epochs)

# cross validation
def crossValidation(X, y):
    skf = StratifiedKFold(n_splits=5)
    clf = make_pipeline(ERPCovariances(estimator='lwf', classes=[1]), MDM())
    return cross_val_score(clf, X, y, cv=skf, scoring='roc_auc').mean()

def classify2012(dataset):
    scr = {}
    # get the data from subject of interest
    # for subject in dataset.subject_list:
    for subject in [1]:

        print('running subject', subject)

        data = dataset._get_single_subject_data(subject)
        raw = data['session_1']['run_training']

        baseFilter(raw, 1, 24)
        events, epochs = epoching(raw, 1, 2, 0.0, 0.1)

        # get trials and labels
        X = epochs.get_data()
        y = events[:, -1]
        y = LabelEncoder().fit_transform(y)

        scr[subject] = crossValidation(X, y)
    
    return scr

def classify2013(dataset):
    scores = {}

    # get the data from subject of interest
    for subject in [8]:
        
        print('running subject', subject)

        scores[subject] = {}

        data = dataset._get_single_subject_data(subject)

        for session in data.keys():			

            print('running session', session)

            raw = data[session]['run_3']

            baseFilter(raw, 1, 24)

            events, epochs = epoching(raw, 33286, 33285, 0.0, 0.1)

            # get trials and labels
            X = epochs.get_data()
            y = events[:, -1]
            y[y == 33286] = 0
            y[y == 33285] = 1

            scr = crossValidation(X, y)

            scores[subject][session] = scr.mean()

    return scores

def classify2014a(dataset):
    scr = {}
    for subject in [1]:

        #load data
        print('running subject', subject)
        sessions = dataset._get_single_subject_data(subject)
        raw = sessions['session_1']['run_1']

        baseFilter(raw, 1, 20)
        events, epochs = epoching(raw, 1, 2, 0.0, 0.8)

        # get trials and labels
        X = epochs.get_data()
        y = epochs.events[:,-1]
        y = y - 1

        scr[subject] = crossValidation(X, y)

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
                pick_channels = raw_solo.ch_names[0:32] + [raw_solo.ch_names[-1]]
            elif subject == 2:
                pick_channels = raw_solo.ch_names[32:-1] + [raw_solo.ch_names[-1]]        
            raw_solo.pick_channels(pick_channels)
            raw_cola = sessions['collaborative']['run_1']
            raw_cola = raw_cola.copy().pick_channels(pick_channels)

            for condition, raw in zip(['solo', 'cola'], [raw_solo, raw_cola]):        

                baseFilter(raw, 0, 20)          
                events, epochs = epoching(raw, 1, 2, 0.0, 0.8)

                # get trials and labels
                X = epochs.get_data()
                y = epochs.events[:,-1]
                y = y - 1

                scores[pair][subject][condition] = crossValidation(X, y)

    return scores

def classify2015a(dataset):
    scr = {}

    # note that subject 31 at session 3 has a few samples which are 'nan'
    # to avoid this problem it could be preferable to dropped the epochs having this condition

    #load data
    for subject in [1]:

        print('running subject', subject)
        sessions = dataset._get_single_subject_data(subject)
        scr[subject] = {}

        for session in sessions.keys():

            print('session', session)
            raw = sessions[session]['run_1']		

            baseFilter(raw, 1, 24)

            events, epochs = epoching(raw, 1, 2, 0.0, 0.8)

            # get trials and labels
            X = epochs.get_data()
            y = epochs.events[:,-1]
            y = y - 1

            scr[subject][session] = crossValidation(X, y)

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
                X = epochs.get_data()
                y = epochs.events[:,-1]
                y = y - 1

                scores[pair][session_name][subject] = crossValidation(X, y)

    return scores

def classsifyAlphaWaves(dataset):
    scr = {}
    for subject in dataset.subject_list[0:2]:
        print('subject', subject)
        raw = dataset._get_single_subject_data(subject)

        # filter data and resample
        baseFilter(raw, 3, 40)
        raw.resample(sfreq=128, verbose=False)

        events, epochs = epoching(raw, 1, 2, 2.0, 8.0, 'closed', 'open')

        # get trials and labels
        X = epochs.get_data()
        y = events[:, -1]

        skf = StratifiedKFold(n_splits=5)
        clf = make_pipeline(Covariances(estimator='lwf'), MDM())
        scr[subject] = cross_val_score(clf, X, y, cv=skf).mean()

    return scr

# load BrainInvaders instance

# dataset_2012 = BrainInvaders2012(Training=True)
# scr = classify2012(dataset_2012)

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

dataset_alphaWaves = AlphaWaves(useMontagePosition=False)
scr = classsifyAlphaWaves(dataset_alphaWaves)

print(scr)
