#!/usr/bin/env sage

import os
from pathlib import Path

from setuptools import setup, find_packages

from curve_analyzer.definitions import TEST_PATH

install_requires = [
    'sage',
    'sarge',
    'psutil',
    'pid>=2.0.1',
    'coloredlogs',
    'shellescape',
]

setup(name='DiSSECT',
      version='0.2',
      description='Distinguisher of Standard & Simulated Elliptic Curves through Testing.',
      url='https://gitlab.fi.muni.cz/x408178/curve_analyzer',
      author='SeSuSy',
      # author_email='email',
      license='MIT',
      packages=find_packages(),
      install_requires = install_requires
      )

os.system(Path(TEST_PATH,"gen_params.py"))
os.system(Path(TEST_PATH,"gen_test_structures.py"))
