#!/usr/bin/env python3
# =.- coding: utf-8 -.-

from __future__ import absolute_import
from __future__ import print_function

from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from setuptools import find_packages
from setuptools import setup
import io
import os
import pathlib
import re

HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

version = '0.0.5'
# if os.environ.get('CI_COMMIT_TAG'):
#     version = os.environ['CI_COMMIT_TAG']
# else:
#     # export this env-var (OMIC_PI_VERSION) if locally deploying, 
#     # if using ci/cd, remember increment it if not deploying from ci/cd git tag
#     # or deploy from git commit tag to auto use (CI_COMMIT_TAG)
#     version = os.environ['OMIC_PI_VERSION']  

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name='omic',
    version=version,
    description='Official Omic client.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://omic.ai',
    author='Luke Weber',
    author_email='luke@omic.ai',
    license='MIT',
    python_requires='>=3.6',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=[
        'pytest-runner',
    ],
    include_package_data=True,
    install_requires=install_requires,
)
