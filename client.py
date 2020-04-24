
from ast import literal_eval
import http.client
import os
import time
import subprocess
from terminal_symbols import FOR, ASSIGNATION, LIST_SEPARATOR, SEPARATOR, \
    CACHE, USING, GET_SCORES_IN

DATABASES = 1
VALUES = 0


def startAndWaitForServer():
    subprocess.Popen(["python", "api.py"])
    while not os.path.exists("server.lock"):
        time.sleep(0.1)
    return


def __write_condition__(bdds, bdd, valuesAndDatabase, key):
    bdds[bdd] = True
    _for = FOR + ' ' + bdd
    return key + ASSIGNATION + \
        str(valuesAndDatabase[VALUES]).replace(',', LIST_SEPARATOR) + \
        ' ' + _for + SEPARATOR + ' '


class ClientRequest():

    def __init__(self):
        self.pload = ""
        self.isCache = True
        self.using = {}
        startAndWaitForServer()

    def useCache(self, isCache):
        self.isCache = isCache

    def __contains__(self, key):
        return key in self.using

    def __getitem__(self, key):
        return self.using[key]

    def __setitem__(self, key, valuesAndDatabase):
        self.using[key] = valuesAndDatabase

    def __build_pload__(self):
        self.pload = CACHE + ' ' if self.isCache else ''
        self.pload += GET_SCORES_IN

        bdds = {}
        conditions = ''
        for key, valuesAndDatabase in self.using.items():
            _for = ''
            bdd = valuesAndDatabase[DATABASES]
            if(not type(bdd) == list):
                conditions += __write_condition__(bdds,
                                                  bdd, valuesAndDatabase, key)
            else:
                for b in bdd:
                    conditions += __write_condition__(bdds,
                                                      b, valuesAndDatabase, key)

        for key in bdds:
            self.pload += ' ' + key + SEPARATOR
        self.pload = self.pload[0:-1]
        self.pload += ' ' + USING + ' ' + conditions
        self.pload = self.pload[0:-2]

    def execute(self, str_request=None):
        if(str_request == None):
            self.__build_pload__()
        else:
            self.pload = str_request
        connection = http.client.HTTPConnection("localhost:8585")
        connection.request("GET", "/request?" + self.pload.replace(" ", "%20"))
        response = connection.getresponse()
        connection.close()

        return literal_eval(response.readline().decode("utf-8"))


# request = ClientRequest()
# request.useCache(True)
# request['subject'] = ([1], BI_2012)
# request['tmax'] = ([0.7], BI_2012)

# print(request.execute())

# print(request.execute(
#     "@cache get-scores-in bi2012 using subject=[1], tmax=[0.7]"))
