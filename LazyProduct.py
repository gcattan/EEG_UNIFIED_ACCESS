def getDicoKeys(*names):
        return names

class LazyProduct():

    def __init__(self, **arrays):
        self.arrays = arrays
        self.size = len(arrays)
        self.iteratorName = getDicoKeys(*arrays)
        self.iterators = [1] *  self.size
        self.arrayLen = []
        self.numberOfElements = 1
        self.sumMax = 0
        for i in range(0, self.size):
            self.arrayLen.append(len(arrays[self.iteratorName[i]]))
            self.numberOfElements = self.numberOfElements * (self.arrayLen[i])
        print('ok')
    
    def hasNext(self):
        return not self.sumMax == self.size

    def next(self):
        self.iterators[0] += 1
        for i in range(0, self.size):
            iterator = self.iterators[i]
            if(iterator > self.arrayLen[i]):
                
                if(not i == self.size - 1):
                    self.iterators[i] = 1
                    self.sumMax -= 1
                    self.iterators[i + 1] = self.iterators[i + 1] + 1
                else:
                    self.iterators[i] = 1
            else:
                if(iterator == self.arrayLen[i]):
                    self.sumMax += 1
                return
    
    def get(self, iteratorName):
        return self.arrays[iteratorName][self.iterators[self.iteratorName.index(iteratorName)] - 1]

    

lz = LazyProduct(first = [1, 2], second = ['a', 'b'], third = ['#', '%', 'km'])
print(lz.iterators)
print(lz.get('first'), lz.get('second'), lz.get('third'))
while(lz.hasNext()):
    lz.next()
    print(lz.get('first'), lz.get('second'), lz.get('third'))

