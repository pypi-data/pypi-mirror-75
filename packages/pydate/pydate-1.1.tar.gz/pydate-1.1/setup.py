#!/usr/bin/env python3
# Setup python package - python setup.py sdist

from setuptools import setup, find_packages

setup(
    name='pydate',
    version='1.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Package made to format date & time strings for use in various SQL RDBMS',
    long_description=open('README.txt').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CodeConfidant/pydate-time',
    author='Drew Hainer',
    author_email='codeconfidant@gmail.com',
    platforms=['Windows', 'Linux']
)