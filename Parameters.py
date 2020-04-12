from lazy_product import LazyProduct as lz
from sklearn.model_selection import KFold
import numpy as np
import random


def __toVariadicArgs__(**args):
    return args


time_low = __toVariadicArgs__(tmin=[0.0], tmax=[0.8])
freq_std = __toVariadicArgs__(fmin=[1], fmax=[24])
freq_strict = __toVariadicArgs__(fmin=[1], fmax=[20])
freq_high = __toVariadicArgs__(fmin=[1], fmax=[35])
freq_large = __toVariadicArgs__(fmin=[3], fmax=[40])
all_sbj_in_pair = __toVariadicArgs__(subject=[1, 2])
all_sessions = __toVariadicArgs__(session='all')
all_pairs = __toVariadicArgs__(pair='all')
dwnsplg_high = __toVariadicArgs__(fs=[128])
with_cov = __toVariadicArgs__(validation=['cov'])


def __base_dflts__(condition=['Target'], tmin=[0.0], tmax=[1.0], fs=[None],
                   subject='all', fmin=[1], fmax=[24], validation=['erp_cov']):
    return locals()


def getDefaultBi2012():
    return __toVariadicArgs__(**__base_dflts__())


def getDefaultBi2013():
    return __toVariadicArgs__(**__base_dflts__(), **all_sessions)


def getDefaultBi2014a():
    return __toVariadicArgs__(**__base_dflts__(**time_low, **freq_strict))


def getDefaultBi2014b():
    return __toVariadicArgs__(**__base_dflts__(**time_low, **freq_strict, **all_sbj_in_pair),
                              **all_pairs, xpdesign=['cola', 'solo'])


def getDefaultBi2015a():
    return __toVariadicArgs__(**__base_dflts__(**time_low, **freq_std), **all_sessions)


def getDefaultBi2015b():
    return __toVariadicArgs__(**__base_dflts__(**time_low, **freq_strict, **all_sbj_in_pair),
                              **all_sessions, **all_pairs)


def getDefaultAlpha():
    return __toVariadicArgs__(**__base_dflts__(condition=['closed'], tmin=[2.0], tmax=[8.0],
                                               **dwnsplg_high, **freq_large, **with_cov))


def getDefaultPHMD():
    return __toVariadicArgs__(**__base_dflts__(condition=['OFF'], tmin=[10], tmax=[50],
                                               **dwnsplg_high, **freq_high, **with_cov))


def getDefaultVR():
    return __toVariadicArgs__(**__base_dflts__(validation=['erp_cov_vr_pc']),
                              repetitions=[[1, 2]], nsplits=[6], xpdesign=['VR'])


class Parameters():
    def __init__(self, useCache, **args):
        self.useCache = useCache
        self.params = args

    def __computeSubjects__(self, dataset):
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

    def __computeSession2013__(self):
        session = self.params['session']
        if session == 'all':
            return ['session_1', 'session_2', 'session_3', 'session_4',
                    'session_5', 'session_6', 'session_7', 'session_8']
        return ['session_' + str(x) for x in session]

    def __computeSession2015a__(self):
        session = self.params['session']
        if session == 'all':
            return ['session_1', 'session_2', 'session_3']
        return ['session_' + str(x) for x in session]

    def __computeSession2015b__(self):
        session = self.params['session']
        if session == 'all':
            return ['s1', 's2', 's3', 's4']
        return ['s' + str(x) for x in session]

    def __computeTrainAndTest__(self):
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
        return __toVariadicArgs__(condition=self.params['condition'], tmin=self.params['tmin'], tmax=self.params['tmax'],
                                  fs=self.params['fs'], subject=self.__computeSubjects__(
                                      dataset), validation=self.params['validation'],
                                  fmin=self.params['fmin'], fmax=self.params['fmax'])

    def getBi2012(self, dataset):
        return lz(bdd=['bi2012'], **self.__base__(dataset))

    def getBi2013(self, dataset):
        return lz(bdd=['bi2013'], **self.__base__(dataset),
                  session=self.__computeSession2013__())

    def getBi2014a(self, dataset):
        return lz(bdd=['bi2014a'], **self.__base__(dataset))

    # subject/ 1 or 2. Pair = same as subject for other datasets
    def getBi2014b(self, dataset):
        return lz(bdd=['bi2014b'], **self.__base__(dataset, subject=self.params['subject']),
                  pair=self.__computeSubjects__(dataset), xpdesign=['cola', 'solo'])

    def getBi2015a(self, dataset):
        return lz(bdd=['bi2015a'], **self.__base__(dataset),
                  session=self.__computeSession2015a__())

    def getBi2015b(self, dataset):
        return lz(bdd=['bi2015b'], **self.__base__(dataset, subject=self.params['subject']),
                  pair=self.__computeSubjects__(dataset), session=self.__computeSession2015b__())

    def getAlpha(self, dataset):
        return lz(bdd=['alpha'], **self.__base__(dataset))

    def getPHMD(self, dataset):
        return lz(bdd=['PHMD'], **self.__base__(dataset))

    def getVR(self, dataset):
        self.__computeTrainAndTest__()
        return lz(bdd=['VR'], **self.__base__(dataset),
                  repetitions=self.params['repetitions'], subset=self.params['subset'], xpdesign=self.params['xpdesign'])
