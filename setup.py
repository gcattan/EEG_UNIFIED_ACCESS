import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eeguni-GCATTAN", # Replace with your own username
    version="0.1",
    author="Gregoire Cattan",
    author_email="gcattan@hotmail.fr",
    description="A server/client wrapper for EEG datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gcattan/EEG_UNIFIED_ACCESS.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering"
    ],
    python_requires='>=3.6',
)