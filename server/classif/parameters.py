"""
This module provides LazyProduct for all datasets.

Acceptable parameters are:
- tmin: epoch start time (0 = onset of the stimulation) in ms [all];
 eg tmin = [0, 10]
- tmax: epoch end time (0 = onset of the stimulation) in ms [all];
 eg tmax = [500, 1000]
- fmin: minium frequence of the bandpass filter [all];
 eg fmin = [1, 2]
- fmax: maximum frequence of the bandpass filter [all];
 eg fmax = [20, 35]
- subject: list of subjects to be included [all];
 eg subject = [1, 2, 3] or subjet = 'all'
 note that when the 'pair' parameter is enabled, the number of subject cannot be greater than 2
- session: list of session to be included [bi2013, bi2015a, bi2015b];
 eg session = [1, 2, 3] or session = 'all'
- pair: when subjects in experiments are paired, the list of pairs to be included [bi2014b, bi2015b]
 eg pair = [1, 2, 3] or pair = 'all'
- fs: sampling frequency [all];
 eg fs = [None] or fs = [124, 256]
- validation: classification method to use. There are in classification.py [all];
 eg validation = ['erp_cov']
 note that you can also use custom python function written as strings:
  validation_method = "your awsome function"
  validation = {validation_method}
- condition: list of conditions, such as condition = [conditionA, conditionB, ...];
 for alpha dataset, values are 'closed' or 'open'
 for phmd dataset, values are 'ON' or 'OFF'
 for others dataset, values are Target or NonTarget
- adaptive: if true select epochs with adaptive training [bi2013]
- nonadaptive: if true select epochs with nonadaptive training [bi2013];
 examples: nonadaptive=[True], adaptive=[False]
- training: if true select training epochs [bi2013]
- online: if true select online epochs [bi2013]
 examples: training=[True], online=[False]
- xpdesign: specific to [vr] and [bi2014b];
 eg xpdesign=['VR' or 'PC']; xpdesign = ['solo', 'cola']
- repetitions: specific to [vr] dataset;
 eg repetitions=[[1, 2], [3, 4, 5]] -> average epoch for classification will be computed
 on the basis of repetitions 1 and 2, then using repetitions 3 to 5
- nsplits: specific to [vr] dataset; precise the number of KFold split (for crossvalidation)
 
"""

# This is a workaround to run this module either from main.py or api.py script
try:
    from ..utils.lazy_product import LazyProduct as lz
except:
    from utils.lazy_product import LazyProduct as lz
    
from sklearn.model_selection import KFold
import numpy as np
import random
import sys


def __to_variadic_args__(**args):
    return args

# We define bellow a set of default parameters
time_low = __to_variadic_args__(tmin=[0.0], tmax=[0.8])
freq_std = __to_variadic_args__(fmin=[1], fmax=[24])
freq_strict = __to_variadic_args__(fmin=[1], fmax=[20])
freq_high = __to_variadic_args__(fmin=[1], fmax=[35])
freq_large = __to_variadic_args__(fmin=[3], fmax=[40])
all_sbj_in_pair = __to_variadic_args__(subject=[1, 2])
all_sessions = __to_variadic_args__(session='all')
all_pairs = __to_variadic_args__(pair='all')
dwnsplg_high = __to_variadic_args__(fs=[128])
with_cov = __to_variadic_args__(validation=['cov'])


def __base_dflts__(condition=['Target'], tmin=[0.0], tmax=[1.0], fs=[None],
                   subject='all', fmin=[1], fmax=[24], validation=['erp_cov']):
    return locals()

# bi2012 accepts the following parameter
def get_dflt_bi2012():
    return __to_variadic_args__(**__base_dflts__(), training=[True])


def get_dflt_bi2013():
    return __to_variadic_args__(**__base_dflts__(), **all_sessions,
                                nonadaptive=[True], adaptive=[False], training=[True], online=[False])


def get_dflt_bi2014a():
    return __to_variadic_args__(**__base_dflts__(**time_low, **freq_strict))


def get_dflt_bi2014b():
    return __to_variadic_args__(**__base_dflts__(**time_low, **freq_strict, **all_sbj_in_pair),
                                **all_pairs, xpdesign=['cola', 'solo'])


def get_dflt_bi2015a():
    return __to_variadic_args__(**__base_dflts__(**time_low, **freq_std), **all_sessions)


def get_dflt_bi2015b():
    return __to_variadic_args__(**__base_dflts__(**time_low, **freq_strict, **all_sbj_in_pair),
                                **all_sessions, **all_pairs)


def get_dflt_alpha():
    return __to_variadic_args__(**__base_dflts__(condition=['closed'], tmin=[2.0], tmax=[8.0],
                                                 **dwnsplg_high, **freq_large, **with_cov))


def get_dflt_phmd():
    return __to_variadic_args__(**__base_dflts__(condition=['OFF'], tmin=[10], tmax=[50],
                                                 **dwnsplg_high, **freq_high, **with_cov))


def get_dflt_vr():
    return __to_variadic_args__(**__base_dflts__(validation=['erp_cov_vr_pc']),
                                repetitions=[[1, 2]], nsplits=[6], xpdesign=['VR'])


def get_dflt(bdd):
    return getattr(sys.modules[__name__], "get_dflt_" + bdd)()

class Parameters():

    # This object convert parameters into LazyProduct
    def __init__(self, use_cache, **args):
        # if true, we will use cached result if available
        self.use_cache = use_cache
        self.params = args

    def __compute_subjects__(self, dataset):
        dataset_subjects = dataset.subject_list
        if 'pair' in self.params:
            subject = self.params['pair']
        else:
            subject = self.params['subject']
        if subject == 'all':
            return dataset_subjects
        if type(subject) is int:
            return random.sample(dataset_subjects, int(subject))
        if '%' in subject and len(subject) == 3:
            percent = int(subject[0:2])
            numberOfsubjects = len(dataset_subjects) - 1
            return random.sample(dataset_subjects, int(numberOfsubjects * percent / 100))
        return subject

    def __compute_paired_subject(self):
        subject = self.params['subject']
        if subject == 'all':
            return [1, 2]
        return subject

    def __compute_session_2013__(self):
        session = self.params['session']
        if session == 'all':
            return ['session_1', 'session_2', 'session_3', 'session_4',
                    'session_5', 'session_6', 'session_7', 'session_8']
        return ['session_' + str(x) for x in session]

    def __compute_session_2015a__(self):
        session = self.params['session']
        if session == 'all':
            return ['session_1', 'session_2', 'session_3']
        return ['session_' + str(x) for x in session]

    def __compute_session_2015b__(self):
        session = self.params['session']
        if session == 'all':
            return ['s1', 's2', 's3', 's4']
        return ['s' + str(x) for x in session]

    def __compute_train_and_test__(self):
        subset = []
        blocks = np.arange(1, 13)
        indexes = np.arange(12)
        for n in self.params['nsplits']:
            kf = KFold(n_splits=n)
            for train_idx, test_idx in kf.split(indexes):
                subset.append(
                    {'train': blocks[train_idx], 'test': blocks[test_idx]})
        self.params['subset'] = subset

    def __base__(self, dataset, subject=None):
        return __to_variadic_args__(condition=self.params['condition'], tmin=self.params['tmin'], tmax=self.params['tmax'],
                                    fs=self.params['fs'], subject=self.__compute_subjects__(
            dataset) if subject == None else subject, validation=self.params['validation'],
            fmin=self.params['fmin'], fmax=self.params['fmax'])

    def get_bi2012(self, dataset):
        return lz(bdd=['bi2012'], **self.__base__(dataset), training=self.params['training'])

    def get_bi2013(self, dataset):
        return lz(bdd=['bi2013'], **self.__base__(dataset),
                  session=self.__compute_session_2013__(),
                  nonadaptive=self.params['nonadaptive'], adaptive=self.params['adaptive'],
                  training=self.params['training'], online=self.params['online'])

    def get_bi2014a(self, dataset):
        return lz(bdd=['bi2014a'], **self.__base__(dataset))

    # subject/ 1 or 2. Pair = same as subject for other datasets
    def get_bi2014b(self, dataset):
        return lz(bdd=['bi2014b'], **self.__base__(dataset, subject=self.__compute_paired_subject()),
                  pair=self.__compute_subjects__(dataset), xpdesign=['cola', 'solo'])

    def get_bi2015a(self, dataset):
        return lz(bdd=['bi2015a'], **self.__base__(dataset),
                  session=self.__compute_session_2015a__())

    def get_bi2015b(self, dataset):
        return lz(bdd=['bi2015b'], **self.__base__(dataset, subject=self.__compute_paired_subject()),
                  pair=self.__compute_subjects__(dataset), session=self.__compute_session_2015b__())

    def get_alpha(self, dataset):
        return lz(bdd=['alpha'], **self.__base__(dataset))

    def get_phmd(self, dataset):
        return lz(bdd=['PHMD'], **self.__base__(dataset))

    def get_vr(self, dataset):
        self.__compute_train_and_test__()
        return lz(bdd=['VR'], **self.__base__(dataset),
                  repetitions=self.params['repetitions'], subset=self.params['subset'], xpdesign=self.params['xpdesign'])

    def __str__(self):
        return str({'cache': self.use_cache, 'params': self.params})

    def __repr__(self):
        return self.__str__()
