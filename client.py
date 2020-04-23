
from ast import literal_eval
import http.client
import os
import time
import subprocess

BI_2012 = "bi2012"
BI_2013 = "bi2013"
BI_2014a = "bi2014a"
BI_2014b = "bi2014b"
BI_2015a = "bi2015a"
BI_2015b = "bi2015b"
ALPHA = "alpha"
PHMD = "phmd"
VR = "vr"

BIs = [BI_2012, BI_2013, BI_2014a, BI_2014b, BI_2015a, BI_2015b]
ALPHAs = [ALPHA, PHMD]
ERPs = [*BIs, VR]
ALL = [*ERPs, *ALPHAs]


GET_SCORES_IN = "get-scores-in"
USING = "using"
SEPARATOR = ","
ASSIGNATION = "="
LIST_SEPARATOR = ";"
LIST_BRAC_IN = "["
LIST_BRAC_OUT = "]"
CACHE = "@cache"
FOR = 'for'


def startAndWaitForServer():
    subprocess.Popen(["python", "api.py"])
    while not os.path.exists("server.lock"):
        time.sleep(0.1)
    return


def __write_condition__(bdds, bdd, value, key):
    bdds[bdd] = True
    _for = FOR + ' ' + bdd
    return key + ASSIGNATION + \
        str(value[0]).replace(',', LIST_SEPARATOR) + \
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

    def __setitem__(self, key, value):
        self.using[key] = value

    def __build_pload__(self):
        self.pload = CACHE if self.isCache else ''
        self.pload += ' ' + GET_SCORES_IN

        bdds = {}
        conditions = ''
        for key, value in self.using.items():
            _for = ''
            bdd = value[1]
            if(not type(bdd) == list):
                conditions += __write_condition__(bdds, bdd, value, key)
            else:
                for b in bdd:
                    conditions += __write_condition__(bdds, b, value, key)

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
        print(self.pload)
        connection = http.client.HTTPConnection("localhost:8585")
        connection.request("GET", "/request?" + self.pload.replace(" ", "%20"))
        response = connection.getresponse()
        connection.close()

        return literal_eval(response.readline().decode("utf-8"))


request = ClientRequest()
request.useCache(True)
request['subject'] = ([1], BI_2013)
request['tmax'] = ([0.7, 0.8, 'VR'], ALL)

print(request.execute())

print(request.execute(
    "@cache get-scores-in bi2012 using subject=[1], tmax=[0.7]"))
