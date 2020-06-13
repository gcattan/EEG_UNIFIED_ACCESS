
from ast import literal_eval
import http.client
import os
import time
import subprocess

# import importlib.util
# spec = importlib.util.spec_from_file_location("terminal_symbols", os.path.dirname(os.path.realpath(__file__))+"\\terminal_symbols.py")
# symbols = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(symbols)

try:
    from terminal_symbols import FOR, ASSIGNATION, LIST_SEPARATOR, SEPARATOR, \
        CACHE, USING, GET_SCORES_IN, WITH
except:
    from .terminal_symbols import FOR, ASSIGNATION, LIST_SEPARATOR, SEPARATOR, \
        CACHE, USING, GET_SCORES_IN, WITH

DATABASES = 1
VALUES = 0


def serverRunning():
    lock_path = os.path.dirname(os.path.realpath(__file__)) + "/server.lock"
    return os.path.exists(lock_path)

# delete lockfile is no instance is using it
def autoclean():
    lock_path = os.path.dirname(os.path.realpath(__file__)) + "/server.lock"
    if(serverRunning()):
        try:
            os.remove(lock_path)
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

# a condition is something such as 'using subject=[1,2]' in the request
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
        self.keywords = []
        self.using = {}
        startAndWaitForServer()

    def useCache(self, isCache):
        self.isCache = isCache

    # Keywords are specific request on the store.
    # See \server\lang\request_interpreter.py [__keywords__]
    # See \server\classif\classification_wrapper.py [run_request]
    def setKeywords(self, keywords):
        self.keywords = keywords

    def __contains__(self, key):
        return key in self.using

    def __getitem__(self, key):
        return self.using[key]

    # in the form request[key] = (values, database); such as request['subject'] = ('all', PHMD)
    def __setitem__(self, key, valuesAndDatabase):
        # valuesAndDatabase is of type Tuple (values, database)
        self.using[key] = valuesAndDatabase

    # build the request to send to the server
    def __build_pload__(self):
        # check if CACHE enable
        self.pload = CACHE + ' ' if self.isCache else ''
        self.pload += WITH + \
            str(self.keywords) + ' ' if len(self.keywords) > 0 else ''
        self.pload += GET_SCORES_IN
        # write condition such as subject = [1,2]
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
