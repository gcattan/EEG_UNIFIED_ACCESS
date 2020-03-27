from LazyProduct import LazyProduct as lz


class Parameters():
    def __init__(self, **args):
        self.params = args

    def getBi2012(self):
        return lz(condition=self.params['condition'], tmin=self.params['tmin'],
                  tmax=self.params['tmax'], resampling=self.params['resampling'],
                  subject=self.params['subject'], fMin=self.params['fMin'], fMax=self.params['fMax'])
