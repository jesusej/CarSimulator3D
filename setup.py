from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name='car-simulator-server',
  version='1.0.0',
  description='Server implementation for car simulator for Unity',
  long_description=long_description,
  url='https://github.com/jesusej/CarSimulator3D',
  license='Apache-2.0'
)