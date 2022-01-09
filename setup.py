#!/usr/bin/env sage

import importlib.util
from pathlib import Path

from setuptools import setup, find_packages

from dissect.definitions import TRAIT_PATH

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name='DiSSECT',
      version='0.3',
      description='Distinguisher of Standard & Simulated Elliptic Curves through Traits.',
      url='https://github.com/crocs-muni/DiSSECT',
      author='Vladimír Sedláček, Vojtěch Suchánek and Antonín Dufka',
      author_email='vlada.sedlacek@mail.muni.cz',
      license='MIT',
      packages=find_packages(),
      install_requires=install_requires,
      entry_points={
          'console_scripts': [
              'dissect-database=dissect.utils.database_handler:main',
              'dissect-compute-database=dissect.traits.run:main',
              'dissect-compute-file=dissect.traits.compute:main',
              'dissect-feature_builder=dissect.analysis.feature_builder:main',
              'dissect-find_outliers=dissect.analysis.find_outliers:main',
              'dissect-detail=dissect.analysis.detail:main'
          ]
      }
)

spec2 = importlib.util.spec_from_file_location("gen_test", Path(TRAIT_PATH, "gen_trait_structures.py"))
gen_trait = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(gen_trait)
gen_trait.main(True)
