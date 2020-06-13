# EEG_UNIFIED_ACCESS (eeguni)
Unified Access to EEG databases recorded at GIPSA-lab.

Current version is 0.0.1 (alpha).

# Disclaimer
This work only provides an wrapper around the libraries listed in the references bellow.
In any matter we are responsible for the accuracy and correctness of these nested libraries.
On the other way, please give credits for these previous works when working with this wrapper.

Also, note that the present project is experimental and we do not guarantee support for the use of this library. 

# Context
In 2018-2019, the GIPSA-lab has released experimental data on nine EEG experiments - please see [here](https://sites.google.com/site/marcocongedo/science/eeg-data?authuser=0) for more detail.

In this project we are providing a simple wrapper based on a local server/client architecture to request these databases for classification purpose.

In other words:
- it is possible to interrogate within the same request the whole databases, thanks to an epurate SQL-like language.
- it is possible to integrate the project in any code by writting a specific client for the language you are using


# Installation

An alpha revision of this project is available in pip:

`pip install eeguni`

Alternatively, you can also download this project from github and set it up using `install.cmd` (Window) or `install.sh` (Linux). Note that these scripts will not populate the project location into the path.

The package dependencies of this project are listed in `requirements.txt`. These can be installed using pip:

`pip install -r requirements.txt`

After installation, open a python terminal and write:

`import clients.python.client`

If no error pop-up, then the project is probably installed properly :)

# Example

Necessary imports:
>from clients.python.client import ClientRequest, join, autoclean

>from clients.python.terminal_symbols import PHMD

Accert that there is only one server running:
>autoclean()

Begin a new request:
>request = ClientRequest()

Use cached results whether they are available:

>request.useCache(True)

Use all subject in database PHMD

>request['subject'] = ('all', PHMD)

Execute request and print result:
>answer = request.execute()

>print(answer)

Wait for the end of the server (server usually shutdown after 10 seconds of inactivity - that is without any request)
>join()

# Notes
Please find bellow a short description of the packages:
- __server.classif__: classification methods used in the example of the nested libraries, which parameters are exposed in this project. In particular, `parameters.py` describes the possible parameters and values for building requests.
- __server.lang__: interpreter for SQL-like request. Note that `terminal_symbols.py` list all the symbols you might used for building a new request, such as the name of the available datasets.
- __server.utils__: result caching and lazy cartesian project implementation - lazy cartesian product is used to simplify for-loop within `classification.py` while itering through all request parameters.
- __clients.python__: implementation of a client in python.
- __server.api__: implementation of a server in python. 

# References

[Short description of datasets](https://sites.google.com/site/marcocongedo/science/eeg-data?authuser=0)

[Mother of all BCI Benchmarks](https://github.com/NeuroTechX/moabb)

[BI.EEG.2012-GIPSA](https://www.google.com/url?q=https%3A%2F%2Fzenodo.org%2Frecord%2F2649006&sa=D&sntz=1&usg=AFQjCNFn_MXNkwABcJdGwyC1_3rmTWk2aQ)

[BI.EEG.2013-GIPSA](https://www.google.com/url?q=https%3A%2F%2Fzenodo.org%2Frecord%2F2645882%23.XLoaC-gzZnI&sa=D&sntz=1&usg=AFQjCNE9JjtUVD1daMRwaga_2YK_vKfBmA)

[bi2014a](https://zenodo.org/record/3266223/)

[bi2014b](https://www.google.com/url?q=https%3A%2F%2Fzenodo.org%2Frecord%2F3267302%23.XR8tQeszapo&sa=D&sntz=1&usg=AFQjCNEq_Q_eJjYnXmmIOncyryRgzoqNag)

[bi2015a](https://www.google.com/url?q=https%3A%2F%2Fzenodo.org%2Frecord%2F3266930%23.XR8sRuszapo&sa=D&sntz=1&usg=AFQjCNFuez6e0171NdtGN-q4m4YU3jYQgQ)

[bi2015b](https://www.google.com/url?q=https%3A%2F%2Fzenodo.org%2Frecord%2F3268762%23.XR8tEuszapo&sa=D&sntz=1&usg=AFQjCNE6DVwYhbVTVIXhG2yQviFwgrjVUw)

[ALPHA.EEG.2017-GIPSA](https://www.google.com/url?q=https%3A%2F%2Fzenodo.org%2Frecord%2F2605110%23.XLX-O1Uzapo&sa=D&sntz=1&usg=AFQjCNGyZFsAh8rECnm4TVzk1s1bsAxWhA)

[PHMDML.EEG.2017-GIPSA](https://www.google.com/url?q=https%3A%2F%2Fzenodo.org%2Frecord%2F2617085%23.XLX-olUzapo&sa=D&sntz=1&usg=AFQjCNG74i9gj8nmtCeeqLhRwTi91w8efw)

[VR.EEG.2018-GIPSA](https://zenodo.org/record/2605205#.XuU1QLxxdPa)