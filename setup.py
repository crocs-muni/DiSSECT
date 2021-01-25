#!/usr/bin/env sage

from pathlib import Path

from setuptools import setup, find_packages

from curve_analyzer.definitions import TRAIT_PATH

install_requires = [
    'sage>=9.0',
    'prettytable',
    'pathlib',
    'pytz',
    'sarge',
    'psutil',
    'pid>=2.0.1',
    'coloredlogs',
    'shellescape',
    'pymongo',
    'pandas'
]

setup(name='DiSSECT',
      version='0.3',
      description='Distinguisher of Standard & Simulated Elliptic Curves through Traits.',
      url='https://gitlab.fi.muni.cz/x408178/curve_analyzer',
      author='Vladimír Sedláček, Vojtěch Suchánek and Antonín Dufka',
      author_email='vlada.sedlacek@mail.muni.cz',
      license='MIT',
      packages=find_packages(),
      install_requires=install_requires,
      entry_points={
          'console_scripts': ['run_traits_single=curve_analyzer.traits.run_traits_single:main',
                              'merge_trait_results=curve_analyzer.traits.merge_trait_results:main',
                              'run_traits=curve_analyzer.traits.run_traits:main']
      },
      scripts=['curve_analyzer/traits/gen_trait_structures.py', 'curve_analyzer/traits/gen_params.py',
               'curve_analyzer/traits/merge_trait_results.py', 'curve_analyzer/traits/gen_unittest.py',
               'curve_analyzer/traits/run_traits.py', 'curve_analyzer/traits/run_traits_single.py']
      )

import importlib.util

spec = importlib.util.spec_from_file_location("gen_params", Path(TRAIT_PATH, "gen_params.py"))
gen_params = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen_params)
gen_params.main()
spec2 = importlib.util.spec_from_file_location("gen_test", Path(TRAIT_PATH, "gen_trait_structures.py"))
gen_trait = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(gen_trait)
gen_trait.main(True)
