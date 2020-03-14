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
from pyriemann.estimation import ERPCovariances
from tqdm import tqdm
import numpy as np
import mne

import warnings
warnings.filterwarnings("ignore")

exit()
def classify(dataset):
    scr = {}
    # get the data from subject of interest
    # for subject in dataset.subject_list:
    for subject in [1,2]:
        print('running subject', subject)
        data = dataset._get_single_subject_data(subject)
        raw = data['session_1']['run_training']

        # filter data and resample
        fmin = 1
        fmax = 24
        raw.filter(fmin, fmax, verbose=False)

        # detect the events and cut the signal into epochs
        events = mne.find_events(raw=raw, shortest_event=1, verbose=False)
        event_id = {'NonTarget': 1, 'Target': 2}
        epochs = mne.Epochs(raw, events, event_id, tmin=0.0, tmax=1.0, baseline=None, verbose=False, preload=True)
        epochs.pick_types(eeg=True)

        # get trials and labels
        X = epochs.get_data()
        y = events[:, -1]
        y = LabelEncoder().fit_transform(y)

        # cross validation
        skf = StratifiedKFold(n_splits=5)
        clf = make_pipeline(ERPCovariances(estimator='lwf', classes=[1]), MDM())
        scr[subject] = cross_val_score(clf, X, y, cv=skf, scoring='roc_auc').mean()
    
    return scr

#load BrainInvaders2012 instance
dataset_2012 = BrainInvaders2012(Training=True)
scr = classify(dataset_2012)
print(scr)
