import json


def __keyContainsKeywords__(key, keywords):
    for kw in keywords:
        if not kw in key:
            return False
    return True


class Store():
    def __init__(self):
        self.f = open('computational_cache.json', 'r+')
        self.cache = json.load(self.f)

    def __getitem__(self, key):
        return self.cache[str(key)]

    def __setitem__(self, key, value):
        self.cache[str(key)] = value

    def __contains__(self, key):
        return str(key) in self.cache

    def select(self, keywords):
        return [(x, self[x]) for x in self.cache if __keyContainsKeywords__(x, keywords)]

    def save(self):
        self.f.seek(0)
        json.dump(self.cache, self.f)
        self.f.truncate()
        self.f.close()


# s = Store()
# print(s)
# s["key"] = "value"
# s.save()
