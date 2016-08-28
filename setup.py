from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name='MTheory',
  version='0.0.1',
  description='Music Theory Boilerplate',
  long_description=long_description,
  url='https://github.com/athuras/MTheory',
  author='Alexander Huras',
  author_email='athuras@gmail.com',
  license='MIT',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3'
    ],
  packages=['MTheory'],
  package_dir={'MTheory': 'MTheory'},
)
