
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Treble.ai
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------

"""Setup script for dbsession."""

# yapf: disable

# Standard library imports
import ast
import os

# Third party imports
from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module='dbsession'):
    """Get version from text file and avoids importing the module."""
    with open(os.path.join(HERE, module, '__init__.py'), 'r') as f:
        data = f.read()
    lines = data.split('\n')
    for line in lines:
        if line.startswith('VERSION_INFO'):
            version_tuple = ast.literal_eval(line.split('=')[-1].strip())
            version = '.'.join(map(str, version_tuple))
            break
    return version


def get_description():
    """Get long description."""
    with open(os.path.join(HERE, 'README.md'), 'r') as f:
        data = f.read()
    return data


REQUIREMENTS = [
    'psycopg2-binary'
]

setup(
  name='dbsession',
  version=get_version(),
  license='MIT',
  description='The python postgreSQL ORM',
  long_description=get_description(),
  long_description_content_type='text/markdown',
  author='imwiwiim90',
  author_email='imwiwiim90@gmail.com',
  url='https://github.com/treble-ai/dbsession',
  keywords=['python', 'postgreSQL', 'ORM', 'psycopg2'],
  packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
  install_requires=REQUIREMENTS,
  include_package_data=True,
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)
