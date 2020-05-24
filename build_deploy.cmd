@echo off
rmdir /s /q dist 
python setup.py sdist 
python -m twine upload --repository testpypi dist/*
cd ..
pip uninstall eeguni-GCATTAN
python -m pip install --no-binary=:all: --index-url https://test.pypi.org/simple/ --no-deps eeguni-GCATTAN
pip uninstall eeguni-GCATTAN
python -m pip install --no-binary=:all: --index-url https://test.pypi.org/simple/ --no-deps eeguni-GCATTAN
python

