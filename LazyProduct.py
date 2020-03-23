def getDicoKeys(*names):
        return names

class LazyProduct():

    def __init__(self, **arrays):
        self.arrays = arrays
        self.size = len(arrays)
        self.iteratorName = getDicoKeys(*arrays)
        self.iterators = [0] *  self.size
        self.arrayLen = []
        self.numberOfElements = 1
        for i in range(0, self.size):
            self.arrayLen.append(len(arrays[self.iteratorName[i]]))
            self.numberOfElements = self.numberOfElements * (self.arrayLen[i])
        print('ok')

    def hasNext(self):
        for i in self.size:
            if(not self.iterators[i] == self.arrayLen[i]):
                return False
        return True
    
    def next(self, iteratorName):
        return # TODO

    

LazyProduct(first = [1, 2], second = ['a', 'b'], third = ['#', '%', 'km'])

