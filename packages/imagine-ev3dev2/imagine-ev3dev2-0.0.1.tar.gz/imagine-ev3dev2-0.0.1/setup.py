from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name='imagine-ev3dev2',
  version='0.0.1',
  description='FLL focused ev3dev2 framework',
  long_description=long_description,
  author='FLL Team # and #38147',
  author_email='team.innova.fll@gmail.com',
  url='https://github.com/innova-fll/imagine',
  download_url = 'https://github.com/innova-fll/imagine/archive/0.0.1.tar.gz',
  license=license
)