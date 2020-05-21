
from ast import literal_eval
import http.client
import os
import time
import subprocess

# import importlib.util
# spec = importlib.util.spec_from_file_location("terminal_symbols", os.path.dirname(os.path.realpath(__file__))+"\\terminal_symbols.py")
# symbols = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(symbols)

if __package__ is None or __package__ == '':
    from terminal_symbols import FOR, ASSIGNATION, LIST_SEPARATOR, SEPARATOR, \
        CACHE, USING, GET_SCORES_IN, WITH
else:
    from .terminal_symbols import FOR, ASSIGNATION, LIST_SEPARATOR, SEPARATOR, \
        CACHE, USING, GET_SCORES_IN, WITH

DATABASES = 1
VALUES = 0


def serverRunning():
    return os.path.exists("server.lock")


def autoclean():
    if(serverRunning()):
        try:
            os.remove("server.lock")
        except:
            print("Failed to delete lock file: server is already running.")


def join():
    while serverRunning():
        time.sleep(0.1)


def startAndWaitForServer():
    if not serverRunning():
    	cwd=os.path.dirname(os.path.realpath(__file__))
    	try:
        	subprocess.Popen(["python3", "../../server/api.py"],cwd=cwd)
    	except:
        	subprocess.Popen(["python", "../../server/api.py"],cwd=cwd)
    	while not serverRunning():
            time.sleep(0.1)


def __write_condition__(bdds, bdd, valuesAndDatabase, key):
    bdds[bdd] = True
    _for = symbols.FOR + ' ' + bdd
    return key + symbols.ASSIGNATION + \
        str(valuesAndDatabase[VALUES]).replace(',', symbols.LIST_SEPARATOR) + \
        ' ' + _for + symbols.SEPARATOR + ' '


class ClientRequest():

    def __init__(self):
        self.pload = ""
        self.isCache = True
        self.keywords = []
        self.using = {}
        startAndWaitForServer()

    def useCache(self, isCache):
        self.isCache = isCache

    def setKeywords(self, keywords):
        self.keywords = keywords

    def __contains__(self, key):
        return key in self.using

    def __getitem__(self, key):
        return self.using[key]

    def __setitem__(self, key, valuesAndDatabase):
        self.using[key] = valuesAndDatabase

    def __build_pload__(self):
        self.pload = symbols.CACHE + ' ' if self.isCache else ''
        self.pload += symbols.WITH + \
            str(self.keywords) + ' ' if len(self.keywords) > 0 else ''
        self.pload += symbols.GET_SCORES_IN

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
            self.pload += ' ' + key + symbols.SEPARATOR
        self.pload = self.pload[0:-1]
        self.pload += ' ' + symbols.USING + ' ' + conditions
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
