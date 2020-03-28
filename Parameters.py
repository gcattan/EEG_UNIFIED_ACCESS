from LazyProduct import LazyProduct as lz
import random


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

    def getBi2012(self, dataset):
        return lz(bdd=['bi2012'], condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], resampling=self.params['resampling'],
                  subject=self.__computeSubjects__(dataset), fMin=self.params['fMin'], fMax=self.params['fMax'])
