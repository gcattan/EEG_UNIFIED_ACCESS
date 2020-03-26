def getDicoKeys(*names):
    return names


class LazyProduct():

    def __init__(self, **arrays):
        self.arrays = arrays
        self.size = len(arrays)
        self.iteratorName = getDicoKeys(*arrays)
        self.iterators = [1] * self.size
        self.iterators[0] = 0
        self.arrayLen = []
        self.numberOfElements = 1
        self.numberOfDoneIteration = 0
        for i in range(0, self.size):
            self.arrayLen.append(len(arrays[self.iteratorName[i]]))
            self.numberOfElements = self.numberOfElements * (self.arrayLen[i])
            self.setIteratorValue(i)

    def __iter__(self):
        return self

    def __next__(self):

        self.iterators[0] += 1
        for i in range(0, self.size):
            iterator = self.iterators[i]
            if(iterator > self.arrayLen[i]):
                if(not i == self.size - 1):
                    self.iterators[i] = 1
                    self.iterators[i + 1] = self.iterators[i + 1] + 1
                    self.setIteratorValue(i)
                else:
                    self.iterators[i] = 1
                    self.setIteratorValue(i)
            else:
                if(self.numberOfDoneIteration == self.numberOfElements):
                    raise StopIteration
                self.setIteratorValue(i)
                self.numberOfDoneIteration += 1
                return self
        raise StopIteration

    def setIteratorValue(self, i):
        setattr(LazyProduct,
                self.iteratorName[i], self.get(self.iteratorName[i]))

    def get(self, iteratorName):
        return self.arrays[iteratorName][self.iterators[self.iteratorName.index(iteratorName)] - 1]


for c in LazyProduct(first=[1, 2], second=['a', 'b'], third=['#', '%', 'km']):
    print(c.first, c.second, c.third)
