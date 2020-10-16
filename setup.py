from setuptools import setup, find_packages
import os

setup(name='curve_analyzer',
      # version='0.1',
      # description='some description',
      # url='#',
      author='SeSuSy',
      # author_email='email',
      # license='MIT',
      packages=find_packages())

os.system("curve_analyzer/utils/parallel/setup.py")
