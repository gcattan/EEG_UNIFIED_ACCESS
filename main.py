from client import ClientRequest, join
from terminal_symbols import BI_2013

request = ClientRequest()
request.useCache(True)
# request.setKeywords(["subject=1", "pair=5"])
request['subject'] = ('all', BI_2013)
# request['tmax'] = ([0.7], BI_2012)
answer = request.execute()
# print(answer)
join()
