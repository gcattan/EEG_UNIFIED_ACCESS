"""
LazyProduct provides a way to iterate through cartesians product of multiple dimensions.
In short, it allows use to replace nested loop by an unique loop, such as:
for a in A:
    for b in B:
        blablabla

->

for lz in LazyProduct(A, B):
    blablabla

Implementation is similar to mixed-radix number, for which each digit as a different dimension.
Given two parameters A and B with respective dimension N and M, and (ai bj) the current combination.
Then the next combination is just (ai bj) + 1, which results in (ai bj+1) if j+1 < M or (ai+1 0) else.
"""

def get_dico_keys(*names):
    return names


class LazyProduct():

    def __init__(self, **arrays):
        self.string_rep = None
        self.arrays = arrays
        self.size = len(arrays)
        self.iterator_name = get_dico_keys(*arrays)
        self.iterators = [1] * self.size
        self.iterators[0] = 0
        self.array_len = []
        self.number_of_elements = 1
        self.number_of_done_iterations = 0
        for i in range(0, self.size):
            self.array_len.append(len(arrays[self.iterator_name[i]]))
            self.number_of_elements = self.number_of_elements * \
                (self.array_len[i])
            self.set_iterator_value(i)

    def __iter__(self):
        return self

    # return the next combination
    def __next__(self):
        self.string_rep = None
        self.iterators[0] += 1
        for i in range(0, self.size):
            iterator = self.iterators[i]
            if(iterator > self.array_len[i]):
                if(not i == self.size - 1):
                    self.iterators[i] = 1
                    self.iterators[i + 1] = self.iterators[i + 1] + 1
                    self.set_iterator_value(i)
                else:
                    self.iterators[i] = 1
                    self.set_iterator_value(i)
            else:
                if(self.number_of_done_iterations == self.number_of_elements):
                    raise StopIteration
                self.set_iterator_value(i)
                self.number_of_done_iterations += 1
                return self
        raise StopIteration

    def set_iterator_value(self, i):
        setattr(LazyProduct,
                self.iterator_name[i], self.get(self.iterator_name[i]))

    def __str__(self):
        if(self.string_rep == None):
            self.string_rep = ""
            for name in self.iterator_name:
                self.string_rep += name + "=" + \
                    str(getattr(LazyProduct, name)) + ";"
        return self.string_rep

    def get(self, iteratorName):
        return self.arrays[iteratorName][self.iterators[self.iterator_name.index(iteratorName)] - 1]
