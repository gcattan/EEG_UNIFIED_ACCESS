from virtualreality.utilities import get_block_repetition
from moabb.paradigms import P300
from sklearn.preprocessing import LabelEncoder
from store import Store
from parameters import *

import numpy as np
import mne
import pandas as pd
import cross_validation


import warnings
warnings.filterwarnings("ignore")

class_info_std = {'Target': 2, 'NonTarget': 1}
class_info_vr = {'Target': 1, 'NonTarget': 0}
class_info_alpha = {'closed': 1, 'open': 2}
class_info_phmd = {'OFF': 1, 'ON': 2}
class_info_2013 = {'Target': 33285, 'NonTarget': 33286}

# filter data and resample


def base_filter(raw, minf, max, fs=None):
    raw.filter(minf, max, verbose=False)
    if(not fs == None):
        raw.resample(fs, verbose=False)

# detect the events and cut the signal into epochs


def epoching(raw, tmin, tmax, event_id):
    events = mne.find_events(raw=raw, shortest_event=1, verbose=False)
    epochs = mne.Epochs(raw, events, event_id, tmin=tmin,
                        tmax=tmax, baseline=None, verbose=False, preload=True)
    epochs.pick_types(eeg=True)
    return (events, epochs)


def get_data(dataset, subject):
    return dataset._get_single_subject_data(subject)


def get_base_trial_and_label(epochs, events):
    y = events[:, -1]
    X = epochs.get_data()
    if(not len(X) == len(y)):
        y = epochs.events[:, -1]
    return X, y


def use_store(params, store, key, validationName, *args):
    validation_method = getattr(cross_validation, validationName)
    if params.use_cache:
        if key in store:
            ret = store[key]
        else:
            ret = validation_method(*args)
            store[key] = ret
            store.save()
    else:
        ret = validation_method(*args)
    return ret


def classify_2012(dataset, params, store):
    scr = {}

    for lz in params.get_bi2012(dataset):

        print('running', lz)
        X, y = [], []
        if not (params, lz) in store:
            dataset.Training = lz.training

            data = get_data(dataset, lz.subject)
            raw = data['session_1']['run_training']

            base_filter(raw, lz.fmin, lz.fmax, lz.fs)
            events, epochs = epoching(
                raw, lz.tmin, lz.tmax, class_info_std)

            # get trials and labels
            X, y = get_base_trial_and_label(epochs, events)

        scr[str(lz)] = use_store(params, store, lz, lz.validation,
                                 X, y, lz.condition, class_info_std)

    return scr


def classify_2013(dataset, params, store):

    scores = {}

    # get the data from subject of interest
    for lz in params.get_bi2013(dataset):

        print('running', lz)
        X, y = [], []
        if not (params, lz) in store:
            dataset.NonAdaptive = lz.nonadaptive
            dataset.Adaptive = lz.adaptive
            dataset.Training = lz.training
            dataset.online = lz.online

            data = get_data(dataset, lz.subject)

            try:
                raw = data[lz.session]['run_3']
            except:
                print('session unknown')
                continue

            base_filter(raw, lz.fmin, lz.fmax, lz.fs)

            events, epochs = epoching(
                raw, lz.tmin, lz.tmax, class_info_2013)

            # get trials and labels
            X, y = get_base_trial_and_label(epochs, events)

        scores[str(lz)] = use_store(params, store, lz, lz.validation,
                                    X, y, lz.condition, class_info_2013)

    return scores


def classify_2014a(dataset, params, store):
    scr = {}

    for lz in params.get_bi2014a(dataset):

        # load data
        print('running subject', lz)
        sessions = get_data(dataset, lz.subject)
        raw = sessions['session_1']['run_1']

        base_filter(raw, lz.fmin, lz.fmax)
        events, epochs = epoching(raw, lz.tmin, lz.tmax, class_info_std)

        # get trials and labels
        X, y = get_base_trial_and_label(epochs, events)

        scr[str(lz)] = use_store(params, store, lz, lz.validation,
                                 X, y, lz.condition, class_info_std)

    return scr


def classify_2014b(dataset, params, store):
    scores = {}

    for lz in params.get_bi2014b(dataset):

        print('running pair', lz)

        sessions = dataset._get_single_pair_data(pair=lz.pair)

        if lz.xpdesign == 'solo':
            try:
                raw = sessions['solo_' + str(lz.subject)]['run_1']
            except:
                print('session unknown')
                continue
        else:
            raw = sessions['collaborative']['run_1']

        pick_channels = raw.ch_names[0 if lz.subject == 1 else 32:
                                     32 if lz.subject == 1 else -1] + [raw.ch_names[-1]]

        raw = raw.copy().pick_channels(pick_channels)

        base_filter(raw, lz.fmin, lz.fmax, lz.fs)
        events, epochs = epoching(raw, lz.tmin, lz.tmax, class_info_std)

        # get trials and labels
        X, y = get_base_trial_and_label(epochs, events)

        scores[str(lz)] = use_store(params, store, lz, lz.validation,
                                    X, y, lz.condition, class_info_std)

    return scores


def classify_2015a(dataset, params, store):

    scr = {}

    # note that subject 31 at session 3 has a few samples which are 'nan'
    # to avoid this problem it could be preferable to dropped the epochs having this condition

    for lz in params.get_bi2015a(dataset):

        print('running', lz)
        sessions = get_data(dataset, lz.subject)

        raw = sessions[lz.session]['run_1']

        base_filter(raw, lz.fmin, lz.fmax, lz.fs)

        events, epochs = epoching(raw, lz.tmin, lz.tmax, class_info_std)

        # get trials and labels
        X, y = get_base_trial_and_label(epochs, events)

        scr[str(lz)] = use_store(params, store, lz, lz.validation,
                                 X, y, lz.condition, class_info_std)

    return scr


def classify_2015b(dataset, params, store):
    scores = {}

    for lz in params.get_bi2015b(dataset):

        print('running', str(lz))
        X, y = [], []
        if not (params, lz) in store:

            sessions = dataset._get_single_pair_data(pair=lz.pair)

            raw = sessions[lz.session]['run_1']

            pick_channels = raw.ch_names[0 if lz.subject == 1 else 32:
                                         32 if lz.subject == 1 else -1] + [raw.ch_names[-1]]

            raw = raw.copy().pick_channels(pick_channels)

            base_filter(raw, lz.fmin, lz.fmax, lz.fs)

            events, epochs = epoching(raw, lz.tmin, lz.tmax, class_info_std)

            # get trials and labels
            X, y = get_base_trial_and_label(epochs, events)

        scores[str(lz)] = use_store(params, store, lz, lz.validation,
                                    X, y, lz.condition, class_info_std)

    return scores


def classify_alpha(dataset, params, store):
    scr = {}
    for lz in params.get_alpha(dataset):
        print('running', lz)
        raw = get_data(dataset, lz.subject)

        base_filter(raw, lz.fmin, lz.fmax, lz.fs)

        events, epochs = epoching(raw, lz.tmin, lz.tmax, class_info_alpha)

        # get trials and labels
        X, y = get_base_trial_and_label(epochs, events)

        scr[str(lz)] = use_store(params, store, lz, lz.validation,
                                 X, y, lz.condition, class_info_alpha)

    return scr


def classify_vr(dataset, params, store):
    # get the paradigm
    paradigm = P300()
    scr = {}
    for lz in params.get_vr(dataset):
        print('running', lz)
        X, y = [], []
        X_training, labels_training, X_test, labels_test = [], [], [], []
        if not (params, lz) in store:

            paradigm.tmax = lz.tmax
            paradigm.tmin = lz.tmin
            paradigm.fmin = lz.fmin
            paradigm.fmax = lz.fmax
            paradigm.resample = lz.fs

            # define the dataset instance
            dataset.VR = True if lz.xpdesign is 'VR' else False
            dataset.PC = True if lz.xpdesign is 'PC' else False

            # get the epochs and labels
            X, labels, meta = paradigm.get_data(dataset, subjects=[lz.subject])
            labels = LabelEncoder().fit_transform(labels)

            # split in training and testing blocks
            X_training, labels_training, _ = get_block_repetition(
                X, labels, meta, lz.subset['train'], lz.repetitions)
            X_test, labels_test, _ = get_block_repetition(
                X, labels, meta, lz.subset['test'], lz.repetitions)

        scr[str(lz)] = use_store(params, store, lz, lz.validation,
                                 X_training, labels_training, X_test, labels_test, lz.condition, class_info_vr)

    return scr


def classify_phmd(dataset, params, store):

    scr = {}
    for lz in params.get_phmd(dataset):

        print('running', lz)
        # get the raw object with signals from the subject (data will be downloaded if necessary)
        raw = get_data(dataset, lz.subject)
        base_filter(raw, lz.fmin, lz.fmax, lz.fs)

        dict_channels = {chn: chi for chi, chn in enumerate(raw.ch_names)}

        # cut the signals into epochs and get the labels associated to each trial

        events, epochs = epoching(raw, lz.tmin, lz.tmax, class_info_phmd)

        X, y = get_base_trial_and_label(epochs, events)

        scr[str(lz)] = use_store(params, store, lz, lz.validation,
                                 X, y, lz.condition, class_info_phmd)

    return scr
