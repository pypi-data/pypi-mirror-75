#!/usr/bin/env python

from setuptools import setup, find_packages

import urltools

setup(
    name = 'urltools',
    version = urltools.__version__,
    description = 'Some functions to parse and normalize URLs.',
    author = 'Original work by Roderick Baier, republished by itzik-h',
    author_email = '',
    license = 'MIT',
    url = 'https://github.com/itzik-h/urltools',
    download_url = 'https://github.com/itzik-h/urltools/archive/0.3.2.tar.gz',
    packages = find_packages(exclude=['tests'])
)
