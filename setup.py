#!/usr/bin/env sage

import os
from pathlib import Path

from setuptools import setup, find_packages

from curve_analyzer.definitions import TEST_PATH

setup(name='DiSSECT',
      version='0.2',
      description='Distinguisher of Standard & Simulated Elliptic Curves through Testing.',
      url='https://gitlab.fi.muni.cz/x408178/curve_analyzer',
      author='SeSuSy',
      # author_email='email',
      license='MIT',
      packages=find_packages())

# os.system(Path(TEST_PATH"curve_analyzer/utils/parallel/setup.py")
os.system(Path(TEST_PATH,"gen_params.py"))
os.system(Path(TEST_PATH,"gen_test_structures.py"))
