echo off
rmdir .\server\braininvaders2012
rmdir .\server\braininvaders2013
rmdir .\server\braininvaders2014a
rmdir .\server\braininvaders2014b
rmdir .\server\braininvaders2015a
rmdir .\server\braininvaders2015b
rmdir .\server\headmounted
rmdir .\server\alphawaves
rmdir .\server\virtualreality
rmdir .\server\moabb
del .\clients\python\terminal_symbols.py
mklink /j ".\server\braininvaders2012" ".\server\dependencies\py.BI.EEG.2012-GIPSA\braininvaders2012"
mklink /j ".\server\braininvaders2013" ".\server\dependencies\py.BI.EEG.2013-GIPSA\braininvaders2013"
mklink /j ".\server\braininvaders2014a" ".\server\dependencies\py.BI.EEG.2014a-GIPSA\braininvaders2014a"
mklink /j ".\server\braininvaders2014b" ".\server\dependencies\py.BI.EEG.2014b-GIPSA\braininvaders2014b"
mklink /j ".\server\braininvaders2015a" ".\server\dependencies\py.BI.EEG.2015a-GIPSA\braininvaders2015a"
mklink /j ".\server\braininvaders2015b" ".\server\dependencies\py.BI.EEG.2015b-GIPSA\braininvaders2015b"
mklink /j ".\server\headmounted" ".\server\dependencies\py.PHMDML.EEG.2017-GIPSA\headmounted"
mklink /j ".\server\alphawaves" ".\server\dependencies\py.ALPHA.EEG.2017-GIPSA\alphawaves"
mklink /j ".\server\virtualreality" ".\server\dependencies\py.VR.EEG.2018-GIPSA\virtualreality"
mklink /j ".\server\moabb" ".\server\dependencies\NeuroTechX.moabb\moabb"
mklink /h ".\clients\python\terminal_symbols.py" ".\server\lang\terminal_symbols.py"