from client import ClientRequest
from terminal_symbols import VR

request = ClientRequest()
request.useCache(True)
request.setKeywords(["subject=1", "pair=5"])
request['subject'] = ('all', VR)
# request['tmax'] = ([0.7], BI_2012)
answer = request.execute()
print(answer)
