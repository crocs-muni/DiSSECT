from setuptools import setup, find_packages
import os

setup(name='DiSSECT',
      version='0.2',
      description='Distinguisher of Standard & Simulated Elliptic Curves through Testing.',
      url='https://gitlab.fi.muni.cz/x408178/curve_analyzer',
      author='SeSuSy',
      # author_email='email',
      license='MIT',
      packages=find_packages())

os.system("curve_analyzer/utils/parallel/setup.py")
