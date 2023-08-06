#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
from os import path
 
import pyPSCF

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
 
# Ceci n'est qu'un appel de fonction. Mais il est trèèèèèèèèèèès long
# et il comporte beaucoup de paramètres
setup(
    name='pyPSCF',
    version=pyPSCF.__version__,
    packages=find_packages(),
    author="Samuël Weber",
    author_email="samuel.weber@univ-grenoble-alpes.fr",
    url='https://gricad-gitlab.univ-grenoble-alpes.fr/webersa/pyPSCF',
    project_urls={
        'Documentation': 'https://pypscf.readthedocs.io/en/latest/',
        'Source': 'https://gricad-gitlab.univ-grenoble-alpes.fr/webersa/pyPSCF',
	},
    description="A Hysplit backtraj and PSCF tool for atmospheric science",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3',
    install_requires=[ "numpy", "pandas", "matplotlib", "scipy", ],
    extras_require={
        "plot":  ["cartopy"],
        },
    # Active la prise en compte du fichier MANIFEST.in
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
 
    # C'est un système de plugin, mais on s'en sert presque exclusivement
    # Pour créer des commandes, comme "django-admin".
    # Par exemple, si on veut créer la fabuleuse commande "proclame-sm", on
    # va faire pointer ce nom vers la fonction proclamer(). La commande sera
    # créé automatiquement. 
    # La syntaxe est "nom-de-commande-a-creer = package.module:fonction".
    # entry_points = {
    #     'console_scripts': [
    #         'pyPSCF-gui = sm_lib.core:proclamer',
    #     ],
    # },
)
