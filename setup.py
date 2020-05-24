import setuptools
from setuptools.command.install import install
from subprocess import check_call

# https://stackoverflow.com/questions/20288711/post-install-script-with-python-setuptools
class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        check_call("pip install -r requirements.txt".split())
        # check_call("python ./server/dependencies/NeuroTechX.moabb/setup.py develop".split())
        

with open("README.md", "r") as fh:
    long_description = fh.read()

# with open("requirements.txt", "r") as fr:
#     requirements = fr.readlines()

setuptools.setup(
    name="eeguni-GCATTAN", # Replace with your own username
    version="5.5",
    author="Gregoire Cattan",
    author_email="gcattan@hotmail.fr",
    description="A server/client wrapper for EEG datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gcattan/EEG_UNIFIED_ACCESS.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering"
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    # install_requires=['mne'],
    python_requires='>=3.6',
    include_package_data=True
)