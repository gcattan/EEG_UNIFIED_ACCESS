
from ast import literal_eval
import http.client
import os
import time
import subprocess


def startAndWaitForServer():
    subprocess.Popen(["python", "api.py"])
    while not os.path.exists("server.lock"):
        time.sleep(0.1)
    return


class ClientRequest():

    def __init__(self, str_request):
        self.pload = str_request
        self.isCache = True
        self.conditions = []
        startAndWaitForServer()

    def useCache(self, isCache):
        self.isCache = isCache

    def execute(self):
        connection = http.client.HTTPConnection("localhost:8585")
        connection.request("GET", "/request?" + self.pload.replace(" ", "%20"))
        response = connection.getresponse()
        connection.close()

        return literal_eval(response.readline().decode("utf-8"))


request = ClientRequest(
    "@cache get-scores-in bi2012 using subject=[1], tmax=[0.7]")
print(request.execute())
