@echo off
set option=%1%
if "%option%"=="-install" (
	cd ..
	@echo on
	python -m pip install --no-binary=:all: --index-url https://test.pypi.org/simple/ --no-deps eeguni-GCATTAN
) else (
	rmdir /s /q dist 
	python setup.py sdist 
	python -m twine upload --repository testpypi dist/*
	cd ..
	pip uninstall eeguni-GCATTAN
	cd eeguni
)
