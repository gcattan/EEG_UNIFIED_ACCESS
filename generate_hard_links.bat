echo off
rmdir braininvaders2012
rmdir braininvaders2013
rmdir braininvaders2014a
rmdir braininvaders2014b
rmdir braininvaders2015a
rmdir braininvaders2015b
rmdir headmounted
rmdir alphawaves
rmdir virtualreality
rmdir moabb
mklink /j "braininvaders2012" ".\py.BI.EEG.2012-GIPSA\braininvaders2012"
mklink /j "braininvaders2013" ".\py.BI.EEG.2013-GIPSA\braininvaders2013"
mklink /j "braininvaders2014a" ".\py.BI.EEG.2014a-GIPSA\braininvaders2014a"
mklink /j "braininvaders2014b" ".\py.BI.EEG.2014b-GIPSA\braininvaders2014b"
mklink /j "braininvaders2015a" ".\py.BI.EEG.2015a-GIPSA\braininvaders2015a"
mklink /j "braininvaders2015b" ".\py.BI.EEG.2015b-GIPSA\braininvaders2015b"
mklink /j "headmounted" ".\py.PHMDML.EEG.2017-GIPSA\headmounted"
mklink /j "alphawaves" ".\server\dependencies\py.ALPHA.EEG.2017-GIPSA\alphawaves"
mklink /j "virtualreality" ".\py.VR.EEG.2018-GIPSA\virtualreality"
mklink /j "moabb" ".\NeuroTechX.moabb\moabb"