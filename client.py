
import http.client
from ast import literal_eval

pload = "@cache get-scores-in bi2012 using subject=[1], tmax=[0.7]"

connection = http.client.HTTPConnection("localhost:8585")
connection.request("GET", "/request?" + pload.replace(" ", "%20"))
response = connection.getresponse()
body = literal_eval(response.readline().decode("utf-8"))
# print("Status: {} and reason: {}".format(response.status, response.reason))
print(body)

connection.close()
