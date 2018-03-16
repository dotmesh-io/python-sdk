#!/usr/bin/env python

"""Datadots API for Python
See:
https://github.com/dotmesh-io/python-sdk
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("pypandoc module not found, couldn't convert MD to RST")
    read_md = lambda f: open(f, 'r').read()

here = path.abspath(path.dirname(__file__))

setup(
    name='datadots-api',
    version='0.1.0',
    description='Datadots API',  
    long_description=read_md('README.md'), 
    url='https://github.com/dotmesh-io/python-sdk', 
    author='Michael Hausenblas',
    author_email='michael.hausenblas@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache 2 License',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(exclude=['test']),
    install_requires=['jsonrpcclient[requests]']
)