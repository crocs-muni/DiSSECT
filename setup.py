#!/usr/bin/env sage

import os
from pathlib import Path

from setuptools import setup, find_packages

from curve_analyzer.definitions import TEST_PATH

install_requires = [
    'sage>=9.0',
    'prettytable',
    'pytz',
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
      author='Vladimír Sedláček and Vojtěch Suchánek',
      author_email='vlada.sedlacek@mail.muni.cz',
      license='MIT',
      packages=find_packages(),
      install_requires=install_requires,
      entry_points={
          'console_scripts': ['run_tests_single=curve_analyzer.run_tests_single:main',
                              'merge_test_results=curve_analyzer.merge_test_results:main']
      }
      )

os.system(Path(TEST_PATH, "gen_params.py"))
os.system(Path(TEST_PATH, "gen_test_structures.py"))
