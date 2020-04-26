from client import ClientRequest
from terminal_symbols import BI_2012, BI_2013, BI_2014a

request = ClientRequest()
request.useCache(True)
request['subject'] = ('all', BI_2014a)
# request['tmax'] = ([0.7], BI_2012)

print(request.execute())
