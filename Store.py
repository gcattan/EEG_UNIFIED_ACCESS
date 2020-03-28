import json


class Store():
    def __init__(self):
        self.f = open('computational_cache.json', 'r+')
        self.cache = json.load(self.f)

    def __getitem__(self, key):
        return self.cache[key]

    def __setitem__(self, key, value):
        self.cache[key] = value

    def __contains__(self, key):
        return key in self.cache

    def save(self):
        self.f.seek(0)
        json.dump(self.cache, self.f)
        self.f.truncate()
        self.f.close()


# s = Store()
# print(s)
# s["key"] = "value"
# s.save()
