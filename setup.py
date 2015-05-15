#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Christopher C. Strelioff <chris.strelioff@gmail.com>
#
# Distributed under terms of the MIT license.

"""setup.py

Setup for resumepy project.
"""
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='resumepy',
    version='0.1',
    description='A Python package for generating resumes from YAML source.',
    long_description=long_description,
    url='https://github.com/cstrelioff/',
    author='Christopher C. Strelioff',
    author_email='chris.strelioff@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='resume YAML HTML LaTeX',
    packages=['resumepy'],
    package_data={'resumepy': ['data/examples/*',
                               'data/templates/*']},
    install_requires=['future', 'jinja2', 'pyyaml'],
    entry_points={
        'console_scripts': ['resumepy=resumepy.process:main_resume',
                            'resumepy_example=resumepy.utils:copy_example'],
    },
)
