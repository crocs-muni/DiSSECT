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
          'console_scripts': ['run_traits_single=dissect.traits.run_traits_single:main',
                              'merge_trait_results=dissect.traits.merge_trait_results:main',
                              'run_traits=dissect.traits.run_traits:main']
      },
      scripts=['dissect/traits/gen_trait_structures.py', 'dissect/traits/gen_params.py',
               'dissect/traits/merge_trait_results.py', 'dissect/traits/gen_unittest.py',
               'dissect/traits/run_traits.py', 'dissect/traits/run_traits_single.py']
      )

spec = importlib.util.spec_from_file_location("gen_params", Path(TRAIT_PATH, "gen_params.py"))
gen_params = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen_params)
gen_params.main()
spec2 = importlib.util.spec_from_file_location("gen_test", Path(TRAIT_PATH, "gen_trait_structures.py"))
gen_trait = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(gen_trait)
gen_trait.main(True)
