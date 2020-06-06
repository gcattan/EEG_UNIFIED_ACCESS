import json
import os

"""
This module store the results of computation in a file called 'computational_cache.json'.
It provides also a way to filter computational results according to a list of keywords passed as arguments.
"""

def __key_contains_keywords__(key, keywords):
    # return ture if the given key in the store contains ALL the keywords passed through arguments.
    for kw in keywords:
        if not kw in key:
            return False
    return True


class Store():
    def __init__(self):
        self.f = open(os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'computational_cache.json'), 'r+')
        self.cache = json.load(self.f)

    def __getitem__(self, key):
        return self.cache[str(key)]

    def __setitem__(self, key, value):
        self.cache[str(key)] = value

    def __contains__(self, key):
        try:
            if(key[0].use_cache):
                return str(key[1]) in self.cache
        except:
            return str(key) in self.cache

    def select(self, keywords):
        if(keywords):
            return [(x, self[x]) for x in self.cache if __key_contains_keywords__(x, keywords)]

    def save(self):
        self.f.seek(0)
        json.dump(self.cache, self.f)
        self.f.truncate()

    def close(self):
        self.f.close()
