#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: 3-clause BSD
import os
from setuptools import setup, find_packages

__version__ = "0.6.5"
NAME = 'tensorpac'
AUTHOR = "Etienne Combrisson"
MAINTAINER = "Etienne Combrisson"
EMAIL = 'e.combrisson@gmail.com'
KEYWORDS = "phase-amplitude coupling pac tensor oscillation meg eeg python"
DESCRIPTION = "Tensor-based Phase-Amplitude Coupling"
URL = 'http://etiennecmb.github.io/tensorpac/'
DOWNLOAD_URL = ("https://github.com/EtienneCmb/tensorpac/archive/v" +
                __version__ + ".tar.gz")
# Data path :
PACKAGE_DATA = {}


def read(fname):
    """Read README and LICENSE."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name=NAME,
    version=__version__,
    packages=find_packages(),
    package_dir={'tensorpac': 'tensorpac'},
    package_data=PACKAGE_DATA,
    include_package_data=True,
    description=DESCRIPTION,
    long_description=read('README.rst'),
    platforms='any',
    setup_requires=['numpy', 'joblib'],
    install_requires=[
        "numpy",
        "scipy",
        "joblib"
    ],
    dependency_links=[],
    author=AUTHOR,
    maintainer=MAINTAINER,
    author_email=EMAIL,
    url=URL,
    download_url=DOWNLOAD_URL,
    license="BSD 3-Clause License",
    keywords=KEYWORDS,
    classifiers=["Development Status :: 5 - Production/Stable",
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: Education',
                 'Intended Audience :: Developers',
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.7"
                 ])
