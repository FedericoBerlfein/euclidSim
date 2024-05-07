from __future__ import print_function

import sys,os,glob,re
import platform
import ctypes
import ctypes.util
import types
import subprocess
import re
import tempfile
import urllib.request as urllib2
import tarfile
import shutil
import setuptools
from setuptools import setup, find_packages

print("Using setuptools version",setuptools.__version__)
print('Python version = ',sys.version)
py_version = "%d.%d"%sys.version_info[0:2]  # we check things based on the major.minor version.

run_dep = ['numpy', 'galsim']

with open('README.md') as file:
    long_description = file.read()

packages = find_packages()
print('packages = ',packages)

def all_files_from(dir, ext=''):
    """Quick function to get all files from directory and all subdirectories
    """
    files = []
    for root, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith(ext) and not filename.startswith('.'):
                files.append(os.path.join(root, filename))
    return files

shared_data = all_files_from('data')
configs = all_files_from('config', '.yaml')

# Read in the version from imsim/_version.py
# cf. http://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
version_file=os.path.join('euclidsim','_version.py')
verstrline = open(version_file, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    euclidsim_version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (version_file,))
print('euclidSim version is %s'%(euclidsim_version))

dist = setup(name="euclidSim",
    version=euclidsim_version,
    author="euclidSim Developers (point of contact: Federico Berlfein)",
    author_email="fberlfei@andrew.cmu.edu",
    description="Image Simulation tools for Euclid-like simulations",
    long_description=long_description,
    license = "",
    url="https://github.com/FedericoBerlfein/euclidSim",
    download_url="https://github.com/FedericoBerlfein/euclidSim/archive/refs/heads/main.zip"%euclidsim_version,
    packages=packages,
    package_data={'euclidsim': shared_data + configs},
    install_requires=run_dep,
    )
