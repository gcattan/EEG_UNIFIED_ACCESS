import json


def __key_contains_keywords__(key, keywords):
    for kw in keywords:
        if not kw in key:
            return False
    return True


class Store():
    def __init__(self):
        self.f = open('server/utils/computational_cache.json', 'r+')
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
