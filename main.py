from braininvaders2012.dataset import BrainInvaders2012
from braininvaders2013.dataset import BrainInvaders2013
from braininvaders2014a.dataset import BrainInvaders2014a
from braininvaders2014b.dataset import BrainInvaders2014b
from braininvaders2015a.dataset import BrainInvaders2015a
from braininvaders2015b.dataset import BrainInvaders2015b
from alphawaves.dataset import AlphaWaves
from headmounted.dataset import HeadMountedDisplay
from virtualreality.dataset import VirtualReality

from store import Store
import parameters as params
import classification
from request_interpreter import interpret

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

# args = params.get_dflt_bi2012()
# params = params.Parameters(True, **args)


def run_request(str_request):
    store = Store()
    request = interpret(str_request)
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
        score = classification.classify_alpha(dataset_phmd, params, store)
        result.update(score)
    store.save()
    return result


request = "@cache get-scores-in bi2012, bi2013 using subject=all, condition=[VR; PC; 1] for bi2012"
run_request(request)
