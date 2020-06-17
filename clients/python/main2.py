from client import ClientRequest, join, autoclean
from terminal_symbols import ERPs

autoclean()
request = ClientRequest()
request.useCache(True)
durations = range(50, 1050, 50)
offsets = range(-500, 550, 50)
tmax = []
tmin = []
for t in offsets:
    tmin.append(t)
    for d in durations:
        value = t + d
        if not value in tmax:
            tmax.append(t + d)


request['subject'] = ('all', ERPs)
request['pair']=('all', ERPs)
request['tmin']=(tmin, ERPs)
request['tmax']=(tmax, ERPs)

answer = request.execute()
print(request.pload)

join()
