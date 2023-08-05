#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
#Following this tutorial https://packaging.python.org/tutorials/packaging-projects/
#pypi-AgENdGVzdC5weXBpLm9yZwIkNjFjYWU5MmMtZDIzZi00Mzk3LWJkYTQtMTk0Njc5ZGMwNGI3AAIleyJwZXJtaXNzaW9ucyI6ICJ1c2VyIiwgInZlcnNpb24iOiAxfQAABiDS0DKfqNq4gZMLnDgJ0GcKOeABXMg2qpSyz0vrgyAcvA
from setuptools import setup, find_packages

import morphonet
 
setup(
 
    name='morphonet',
 
    version="2.0.0.11",
 
    packages=find_packages(),
 
    author="Emmanuel Faure",
 
    author_email="api@morphonet.com",
 
    description="Python API to interact with MorphoNet",
 
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    install_requires= [ "requests", "numpy"] , 

    include_package_data=True, # MANIFEST.in
 
    url='https://gitlab.inria.fr/efaure/MorphoNet',
 
    # MetaData
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Visualization",
    ],

 
)