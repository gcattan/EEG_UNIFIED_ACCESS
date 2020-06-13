@echo off
rmdir /s /q dist 
python setup.py sdist 
REM python -m twine upload --repository testpypi dist/*
python -m twine upload dist/*
cd ..
REM pip uninstall -y eeguni-GCATTAN
pip uninstall -y eeguni
REM python -m pip install --no-binary=:all: --index-url https://test.pypi.org/simple/ --no-deps eeguni-GCATTAN
REM pip uninstall -y eeguni-GCATTAN
REM python -m pip install --no-binary=:all: --index-url https://test.pypi.org/simple/ --no-deps eeguni-GCATTAN
REM python
pip install eeguni
