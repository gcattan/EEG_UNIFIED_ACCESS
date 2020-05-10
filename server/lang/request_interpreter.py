from classif.parameters import Parameters, get_dflt
from lang.terminal_symbols import GET_SCORES_IN, USING, SEPARATOR, ALL, LIST_SEPARATOR, \
    LIST_BRAC_OUT, LIST_BRAC_IN, ASSIGNATION, CACHE, WITH, FUN_BRAC_IN, FUN_BRAC_OUT


def __clean__(string):
    return string.replace(" ", "")  # .replace("\"'", "").replace("'\"", "")


def __btwn__(string, left_limitator, right_limitator):
    return string.split(left_limitator)[1].split(right_limitator)[0]


def __keywords__(string):
    if(WITH in string):
        return [x.replace("'", "") for x in __btwn__(string, WITH + LIST_BRAC_IN, LIST_BRAC_OUT).split(SEPARATOR)]


def __get_bdds__(request):
    return __btwn__(request, GET_SCORES_IN, USING).split(SEPARATOR)


def __get_conditions__(request):
    cdts = request.split(USING)[1].split(SEPARATOR)
    for i in range(0, len(cdts)):
        cdt = cdts[i].split("for")
        if(len(cdt) == 2):
            cdts[i] = (cdt[0], cdt[1])
        else:
            cdts[i] = (cdt[0], ALL)
    return cdts


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def __to_int_if_needed(array):
    for i in range(0, len(array)):
        if(is_int(array[i])):
            array[i] = int(array[i])
        elif(is_float(array[i])):
            array[i] = float(array[i])
    return array


def __interpret_value__(value):
    if FUN_BRAC_IN in value:
        return [__btwn__(value, FUN_BRAC_IN, FUN_BRAC_OUT).replace(";", SEPARATOR).replace("\\n", "\n")[2:-2]]
    if LIST_BRAC_IN in value:
        # if "@FUN" in value:  # workaround for custom validation method
        #     return value.split('')
        return __to_int_if_needed(__btwn__(value, LIST_BRAC_IN,
                                           LIST_BRAC_OUT).split(LIST_SEPARATOR))
    return value


def __get_params_for_bdd__(bdd_name, conditions):
    ret = {}
    for cdt, bdd in conditions:
        if(bdd == bdd_name or bdd == ALL):
            name_value = cdt.split(ASSIGNATION)
            ret[name_value[0]] = __interpret_value__(
                ASSIGNATION.join(name_value[1:]))
    return ret


def __is_cache_request(request):
    return CACHE in request


def __get_params__(bdds, conditions, use_store):
    ret = {}
    for bdd in bdds:
        args = get_dflt(bdd)
        args.update(__get_params_for_bdd__(bdd, conditions))
        ret[bdd] = Parameters(use_store, **args)
    return ret


def interpret(request):
    request = __clean__(request)
    bdds = __get_bdds__(request)
    cdts = __get_conditions__(request)
    use_store = __is_cache_request(request)
    keywords = __keywords__(request)
    return {'request': __get_params__(bdds, cdts, use_store), 'keywords': keywords}


# request = "@cache get-scores-in bi2012, bi2013 using subject=all, condition=[VR; PC; 1] for bi2012"
# response = interpret(request)
# print(response)
