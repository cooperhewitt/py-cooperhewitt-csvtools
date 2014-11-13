#!/usr/bin/env python

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read(),

setup(
    name='cooperhewitt.csvtools',
    namespace_packages=['cooperhewitt'],
    version='0.2',,
    description='Tools for processing CSV files',
    author='Cooper Hewitt Smithsonian Design Museum',
    url='https://github.com/cooperhewitt/py-cooperhewitt-csvtools',
    requires=[],
    packages=packages,
    scripts=[],
    download_url='https://github.com/cooperhewitt/py-cooperhewitt-csvtools/releases/tag/v0.1',
    license='BSD')
