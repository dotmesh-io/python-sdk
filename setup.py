#!/usr/bin/env python

"""Datadots API for Python
See:
https://github.com/dotmesh-io/python-sdk
"""

from setuptools import setup, find_packages
from codecs import open

setup(
    name='datadots-api',
    version='0.1.2',
    description='Datadots API',  
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/dotmesh-io/python-sdk', 
    author='Michael Hausenblas',
    author_email='michael.hausenblas@gmail.com',
    packages=find_packages(
        exclude=['test', 'build', 'dist', 'datadots_api.egg-info']),
    install_requires=[
        'requests',
        'jsonrpcclient[requests]']
)
