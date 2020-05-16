python setup.py sdist bdist_wheel
python -m twine upload --repository testpypi dist/*
REM python -m pip install --index-url https://test.pypi.org/simple/ --no-deps eeguni-GCATTAN