from client import ClientRequest, join, autoclean
from terminal_symbols import ALL

autoclean()

request = ClientRequest()
request.useCache(True)
# request.setKeywords(["subject=1", "pair=5"])
request['subject'] = ('all', ALL)
# request['tmax'] = ([0.7], BI_2012)
answer = request.execute()
print(answer)

join()
