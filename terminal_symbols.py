GET_SCORES_IN = "get-scores-in"
USING = "using"
SEPARATOR = ","
ALL = "all"
ASSIGNATION = "="
LIST_SEPARATOR = ";"
LIST_BRAC_IN = "["
LIST_BRAC_OUT = "]"
CACHE = "@cache"
FOR = 'for'
WITH = "@with"

BI_2012 = "bi2012"
BI_2013 = "bi2013"
BI_2014a = "bi2014a"
BI_2014b = "bi2014b"
BI_2015a = "bi2015a"
BI_2015b = "bi2015b"
ALPHA = "alpha"
PHMD = "phmd"
VR = "vr"

BIs = [BI_2012, BI_2013, BI_2014a, BI_2014b, BI_2015a, BI_2015b]
ALPHAs = [ALPHA, PHMD]
ERPs = [*BIs, VR]
ALL = [*ERPs, *ALPHAs]
