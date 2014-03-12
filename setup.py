#!/usr/bin/env python

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
    setup_requires=[
        'setuptools-git'
    ],
    install_requires=[
        'setuptools >= 1.1.6',
        'requests',
        'pytz',
        'nose',
        'coverage',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Software Development :: Libraries'],
    )
