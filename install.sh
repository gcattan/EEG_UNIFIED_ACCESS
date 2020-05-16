echo off

# git fetch dependencies
git submodule init
git submodule update
git submodule foreach "(git checkout master;git pull)&"

# generate links to dependencies
cp -al "$(pwd)/server/dependencies/py.BI.EEG.2012-GIPSA/braininvaders2012" "$(pwd)/server/braininvaders2012"
cp -al "$(pwd)/server/dependencies/py.BI.EEG.2013-GIPSA/braininvaders2013" "$(pwd)/server/braininvaders2013"
cp -al "$(pwd)/server/dependencies/py.BI.EEG.2014a-GIPSA/braininvaders2014a" "$(pwd)/server/braininvaders2014a"
cp -al "$(pwd)/server/dependencies/py.BI.EEG.2014b-GIPSA/braininvaders2014b" "$(pwd)/server/braininvaders2014b"
cp -al "$(pwd)/server/dependencies/py.BI.EEG.2015a-GIPSA/braininvaders2015a" "$(pwd)/server/braininvaders2015a"
cp -al "$(pwd)/server/dependencies/py.BI.EEG.2015b-GIPSA/braininvaders2015b" "$(pwd)/server/braininvaders2015b"
cp -al "$(pwd)/server/dependencies/py.PHMDML.EEG.2017-GIPSA/headmounted" "$(pwd)/server/headmounted"
cp -al "$(pwd)/server/dependencies/py.ALPHA.EEG.2017-GIPSA/alphawaves" "$(pwd)/server/alphawaves"
cp -al "$(pwd)/server/dependencies/py.VR.EEG.2018-GIPSA/virtualreality" "$(pwd)/server/virtualreality"
cp -al "$(pwd)/server/dependencies/NeuroTechX.moabb/moabb" "$(pwd)/server/moabb"
ln "$(pwd)/server/lang/terminal_symbols.py" "$(pwd)/clients/python/terminal_symbols.py"

#install requirements
pip3 install -r requirements.txt
sudo apt-get install python3-tk
