#!/usr/bin/env python3
# Setup python package - python setup.py sdist

from setuptools import setup, find_packages

setup(
    name='connectwrap',
    version='1.1.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A Python package for SQLite database management & object relational mapping.',
    long_description=open('README.txt').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CodeConfidant/connectwrap-sqlite3',
    author='Drew Hainer',
    author_email='codeconfidant@gmail.com',
    platforms=['Windows', 'Linux']
)