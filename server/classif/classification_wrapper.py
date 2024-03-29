# workaround depending on which script call this module
try:
    from virtualreality.dataset import VirtualReality
    from braininvaders2012.dataset import BrainInvaders2012
    from braininvaders2013.dataset import BrainInvaders2013
    from braininvaders2014a.dataset import BrainInvaders2014a
    from braininvaders2014b.dataset import BrainInvaders2014b
    from braininvaders2015a.dataset import BrainInvaders2015a
    from braininvaders2015b.dataset import BrainInvaders2015b
    from alphawaves.dataset import AlphaWaves
    from headmounted.dataset import HeadMountedDisplay
    from utils.store import Store
    from lang.request_interpreter import interpret
    import classif.parameters as params
    import classif.classification as classification
except:
    from ..braininvaders2012.dataset import BrainInvaders2012
    from ..braininvaders2013.dataset import BrainInvaders2013
    from ..braininvaders2014a.dataset import BrainInvaders2014a
    from ..braininvaders2014b.dataset import BrainInvaders2014b
    from ..braininvaders2015a.dataset import BrainInvaders2015a
    from ..braininvaders2015b.dataset import BrainInvaders2015b
    from ..alphawaves.dataset import AlphaWaves
    from ..headmounted.dataset import HeadMountedDisplay
    from ..virtualreality.dataset import VirtualReality
    from ..utils.store import Store
    from ..lang.request_interpreter import interpret
    from ..classif import parameters as params
    from ..classif import classification
    # import ..classif.parameters as params
    # import ..classif.classification as classification


"""
This module provides an interface between end-point API (api.py) and classification method.
It interprets the request and call the appropriate classification method. 
In addition, it creates also the dataset instances.
"""

dataset_2012 = BrainInvaders2012(Training=True)
dataset_2013 = BrainInvaders2013(
    NonAdaptive=True, Adaptive=False, Training=True, Online=False)
dataset_2014a = BrainInvaders2014a()
dataset_2014b = BrainInvaders2014b()
dataset_2015a = BrainInvaders2015a()
dataset_2015b = BrainInvaders2015b()
dataset_alpha = AlphaWaves(useMontagePosition=False)
dataset_vr = VirtualReality(useMontagePosition=False)
dataset_phmd = HeadMountedDisplay(useMontagePosition=False)


def run_request(str_request):
    store = Store()
    request_and_keywords = interpret(str_request)
    request = request_and_keywords['request']
    # Keywords are used to conduct independant requests on the store.
    # Such results will be returns along with the classification results.
    keywords = request_and_keywords["keywords"]
    result = {}
    if('bi2012' in request):
        params = request['bi2012']
        score = classification.classify_2012(dataset_2012, params, store)
        result.update(score)
    if('bi2013' in request):
        params = request['bi2013']
        score = classification.classify_2013(dataset_2013, params, store)
        result.update(score)
    if('bi2014a' in request):
        params = request['bi2014a']
        score = classification.classify_2014a(dataset_2014a, params, store)
        result.update(score)
    if('bi2014b' in request):
        params = request['bi2014b']
        score = classification.classify_2014b(dataset_2014b, params, store)
        result.update(score)
    if('bi2015a' in request):
        params = request['bi2015a']
        score = classification.classify_2015a(dataset_2015a, params, store)
        result.update(score)
    if('bi2015b' in request):
        params = request['bi2015b']
        score = classification.classify_2015b(dataset_2015b, params, store)
        result.update(score)
    if('alpha' in request):
        params = request['alpha']
        score = classification.classify_alpha(dataset_alpha, params, store)
        result.update(score)
    if('vr' in request):
        params = request['vr']
        score = classification.classify_vr(dataset_vr, params, store)
        result.update(score)
    if('phmd' in request):
        params = request['phmd']
        score = classification.classify_phmd(dataset_phmd, params, store)
        result.update(score)
    selection = store.select(keywords)
    store.close()
    return {'result': result, 'selection': selection}
