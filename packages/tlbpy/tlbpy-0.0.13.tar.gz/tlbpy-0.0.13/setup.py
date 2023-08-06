#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python setup.py sdist bdist_wheel
# twine upload dist/*
# twine upload --skip-existing dist/*

from setuptools import setup, find_packages

import tlbpy

setup(
    name='tlbpy',
    version=tlbpy.__version__,
    packages=find_packages(),
    author="Guitheg",
    description="My personnal toolbox for python",
    long_description=open('README.md').read(),
    # install_requires= ,
    include_package_data=True,
    url='https://github.com/Guitheg/tlbpy',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Education",
    ],
    # C'est un système de plugin, mais on s'en sert presque exclusivement
    # Pour créer des commandes, comme "django-admin".
    # Par exemple, si on veut créer la fabuleuse commande "proclame-sm", on
    # va faire pointer ce nom vers la fonction proclamer(). La commande sera
    # créé automatiquement. 
    # La syntaxe est "nom-de-commande-a-creer = package.module:fonction".
    entry_points = {
        'console_scripts': [
            'helloworld = tlbpy.helloworld:helloworld',
        ],
    },
    license="MIT", 
)