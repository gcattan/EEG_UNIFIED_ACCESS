from LazyProduct import LazyProduct as lz
from sklearn.model_selection import KFold
import numpy as np
import random


def __toVariadicArgs__(**args):
    return args


t0_100 = __toVariadicArgs__(tmin=[0.0], tmax=[1.0])
t10_80 = __toVariadicArgs__(tmin=[0.0], tmax=[0.8])
f1_24 = __toVariadicArgs__(fmin=[1], fmax=[24])
f1_20 = __toVariadicArgs__(fmin=[1], fmax=[20])


def getDefaultBi2012():
    return __toVariadicArgs__(condition=['Target'], **t0_100, fs=[None],
                              subject='all', **f1_24)


def getDefaultBi2013():
    return __toVariadicArgs__(condition='Target', **t0_100, fs=[None],
                              subject='all', **f1_24,
                              session='all')


def getDefaultBi2014a():
    return __toVariadicArgs__(condition=['Target'], **t10_80, fs=[None],
                              subject='all', **f1_20)


def getDefaultBi2014b():
    return __toVariadicArgs__(condition=['Target'], **t10_80, fs=[None],
                              pair='all', **f1_20, subject=[1, 2], xpdesign=['cola', 'solo'])


def getDefaultBi2015a():
    return __toVariadicArgs__(condition=['Target'], **t10_80, fs=[None],
                              subject='all', **f1_24,
                              session='all')


def getDefaultBi2015b():
    return __toVariadicArgs__(condition=['Target'], **t10_80, fs=[None],
                              subject=[1, 2], **f1_20,
                              session='all', pair='all')


def getDefaultAlpha():
    return __toVariadicArgs__(condition=['closed'], tmin=[2.0],
                              tmax=[8.0], fs=[128],
                              subject='all', fmin=[3], fmax=[40])


def getDefaultPHMD():
    return __toVariadicArgs__(condition=['OFF'], tmin=[10],
                              tmax=[50], fs=[128],
                              subject='all', fmin=[1], fmax=[35])


def getDefaultVR():
    return __toVariadicArgs__(condition=['VR'], fs=[None],
                              subject='all', fmin=[1], fmax=[24],
                              repetitions=[[1, 2]], nsplits=[6], **t0_100)


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

    def getBi2012(self, dataset):
        return lz(bdd=['bi2012'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], fs=self.params['fs'],
                  subject=self.__computeSubjects__(dataset), fmin=self.params['fmin'], fmax=self.params['fmax'])

    def getBi2013(self, dataset):
        return lz(bdd=['bi2013'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], fs=self.params['fs'],
                  subject=self.__computeSubjects__(dataset), fmin=self.params['fmin'], fmax=self.params['fmax'],
                  session=self.__computeSession2013__())

    def getBi2014a(self, dataset):
        return lz(bdd=['bi2014a'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], fs=self.params['fs'],
                  subject=self.__computeSubjects__(dataset), fmin=self.params['fmin'], fmax=self.params['fmax'])

    # subject/ 1 or 2. Pair = same as subject for other datasets
    def getBi2014b(self, dataset):
        return lz(bdd=['bi2014b'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], fs=self.params['fs'],
                  pair=self.__computeSubjects__(dataset), fmin=self.params['fmin'], fmax=self.params['fmax'],
                  subject=self.params['subject'], xpdesign=['cola', 'solo'])

    def getBi2015a(self, dataset):
        return lz(bdd=['bi2015a'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], fs=self.params['fs'],
                  subject=self.__computeSubjects__(dataset), fmin=self.params['fmin'], fmax=self.params['fmax'],
                  session=self.__computeSession2015a__())

    def getBi2015b(self, dataset):
        return lz(bdd=['bi2015b'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], fs=self.params['fs'],
                  pair=self.__computeSubjects__(dataset), fmin=self.params['fmin'], fmax=self.params['fmax'],
                  session=self.__computeSession2015b__(), subject=self.params['subject'])

    def getAlpha(self, dataset):
        return lz(bdd=['alpha'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], fs=self.params['fs'],
                  subject=self.__computeSubjects__(dataset), fmin=self.params['fmin'], fmax=self.params['fmax'])

    def getPHMD(self, dataset):
        return lz(bdd=['PHMD'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], fs=self.params['fs'],
                  subject=self.__computeSubjects__(dataset), fmin=self.params['fmin'], fmax=self.params['fmax'])

    def getVR(self, dataset):
        self.__computeTrainAndTest__()
        return lz(bdd=['VR'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], fs=self.params['fs'],
                  subject=self.__computeSubjects__(dataset), fmin=self.params['fmin'], fmax=self.params['fmax'],
                  repetitions=self.params['repetitions'], subset=self.params['subset'])
