#!/usr/bin/env python

import os, re

try:
    from setuptools import setup
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup

version = '0.8.dev0'

setup(
    name='sunburnt',
    version=version,
    description='Python interface to Solr',
    long_description=open('README.rst').read() + "\n" +
                     open('Changelog').read(),
    author='Toby White',
    author_email='toby@timetric.com',
    url='http://opensource.timetric.com/sunburnt/',
    packages=['sunburnt'],
    requires=['httplib2', 'lxml', 'pytz'],
    setup_requires=[
        'setuptools-git'
    ],
    install_requires=[
        'httplib2',
        'lxml',
        'pytz'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Software Development :: Libraries'],
    )
