#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# package setup
#
# ------------------------------------------------

# imports
# -------
import os

# config
# ------
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

# requirements
# ------------
with open('requirements.txt') as f:
    REQUIREMENTS = f.read().strip().split('\n')

TEST_REQUIREMENTS = [
    'pytest',
    'pytest-runner'
]

if os.path.exists('README.md'):
    long_description = open('README.md').read()
else:
    long_description = 'Cocktail Shaker is drug enumeration and expansion library'

ENTRY_POINTS = {
    'console_scripts': [
        'cocktail-shaker = cocktail_shaker.cli:main',
    ],
}

# exec
# ----
setup(
    name="cocktail_shaker",
    version="1.1.8",
    packages=['cocktail_shaker'],
    license='MIT',
    author="Suliman Sharif",
    author_email="sharifsuliman1@gmail.com",
    url="https://www.github.com/Sulstice/Cocktail-Shaker",
    install_requires=REQUIREMENTS,
    long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe=False,
    keywords='cocktail chemistry ligand-design shaker',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
    entry_points=ENTRY_POINTS,
)
