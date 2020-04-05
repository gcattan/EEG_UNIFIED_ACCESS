from LazyProduct import LazyProduct as lz
import random


def __toVariadicArgs__(**args):
    return args


def getDefaultBi2015a():
    return __toVariadicArgs__(condition=['Target'], tmin=[0.0],
                              tmax=[0.8], resampling=[None],
                              subject='all', fMin=[1], fMax=[20],
                              session='all')


def getDefaultBi2015b():
    return __toVariadicArgs__(condition=['Target'], tmin=[0.0],
                              tmax=[0.8], resampling=[None],
                              subject='all', fMin=[1], fMax=[20],
                              session='all')


class Parameters():
    def __init__(self, useCache, **args):
        self.useCache = useCache
        self.params = args

    def __computeSubjects__(self, dataset):
        dataset_subjects = dataset.subject_list
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

    def getBi2012(self, dataset):
        return lz(bdd=['bi2012'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], resampling=self.params['resampling'],
                  subject=self.__computeSubjects__(dataset), fMin=self.params['fMin'], fMax=self.params['fMax'])

    def getDefaultBi2012(self, dataset):
        return lz(bdd=['bi2012'], condition=['Target'], tmin=[0.0],
                  tmax=[1.0], resampling=[None],
                  subject=dataset.subject_list, fMin=[1], fMax=[24])

    def getBi2013(self, dataset):
        return lz(bdd=['bi2013'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], resampling=self.params['resampling'],
                  subject=self.__computeSubjects__(dataset), fMin=self.params['fMin'], fMax=self.params['fMax'],
                  session=self.__computeSession2013__())

    def getDefaultBi2013(self, dataset):
        return lz(bdd=['bi2013'], condition='Target', tmin=[0.0],
                  tmax=[1.0], resampling=[None],
                  subject=dataset.subject_list, fMin=[1], fMax=[24],
                  session=['session_1', 'session_2', 'session_3', 'session_4',
                           'session_5', 'session_6', 'session_7', 'session_8'])

    def getBi2014a(self, dataset):
        return lz(bdd=['bi2014a'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], resampling=self.params['resampling'],
                  subject=self.__computeSubjects__(dataset), fMin=self.params['fMin'], fMax=self.params['fMax'])

    def getDefaultBi2014a(self, dataset):
        return lz(bdd=['bi2014a'], condition=['Target'], tmin=[0.0],
                  tmax=[0.8], resampling=[None],
                  subject=dataset.subject_list, fMin=[1], fMax=[20])

    # subject/ 1 or 2. Pair = same as subject for other datasets
    def getBi2014b(self, dataset):
        return lz(bdd=['bi2014b'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], resampling=self.params['resampling'],
                  pair=self.__computeSubjects__(dataset), fMin=self.params['fMin'], fMax=self.params['fMax'],
                  subject=self.params['subject'], xpdesign=['cola', 'solo'])

    def getDefaultBi2014b(self, dataset):
        return lz(bdd=['bi2014b'], condition=['Target'], tmin=[0.0],
                  tmax=[0.8], resampling=[None],
                  pair=dataset.pair_list, fMin=[0], fMax=[20], subject=[1, 2], xpdesign=['cola', 'solo'])

    def getBi2015a(self, dataset):
        return lz(bdd=['bi2015a'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], resampling=self.params['resampling'],
                  subject=self.__computeSubjects__(dataset), fMin=self.params['fMin'], fMax=self.params['fMax'],
                  session=self.__computeSession2015a__())

    def getBi2015b(self, dataset):
        return lz(bdd=['bi2015b'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], resampling=self.params['resampling'],
                  subject=self.__computeSubjects__(dataset), fMin=self.params['fMin'], fMax=self.params['fMax'],
                  session=self.__computeSession2015b__())
