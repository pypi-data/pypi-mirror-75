#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script"""

from setuptools import setup, find_packages

with open("README.rst", "r") as readme_file:
    readme = readme_file.read()

# todo: edit to include all dependencies

test_requirements = [
    'codecov',
    'pytest',
    'pytest-cov',
]

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='pycellfit',
    version='0.2.0',
    license='MIT',
    author='Nilai Vemula',
    author_email='nilai.r.vemula@vanderbilt.edu',
    description='Python implementation of the CellFIT method of inferring cellular forces',
    url='https://github.com/NilaiVemula/PyCellFIT',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Natural Language :: English"
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
