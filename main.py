from client import ClientRequest, join, autoclean
from terminal_symbols import PHMD

autoclean()
request = ClientRequest()
request.useCache(True)
# request.setKeywords(["subject=1", "pair=5"])

validation_method = """
ret = 0
X = args[0]
y = args[1]
skf = StratifiedKFold(n_splits=5)
clf = make_pipeline(Covariances(estimator='lwf'), MDM())
ret = cross_val_score(clf, X, y, cv=skf).mean()
"""

request['validation'] = ({validation_method}, PHMD)
# request['tmax'] = ([0.7], BI_2012)
answer = request.execute()
print(answer)

join()
