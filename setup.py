#!/usr/bin/env python

import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

wd = os.path.dirname(os.path.abspath(__file__))
os.chdir(wd)
sys.path.insert(1, wd)

name = 'tmdb3'
pkg = __import__('tmdb3')

author, email = pkg.__author__.rsplit(' ', 1)
email = email.strip('<>')

maintainer, maintainer_email = pkg.__maintainer__.rsplit(' ', 1)
maintainer_email = maintainer_email.strip('<>')

version = pkg.__version__
classifiers = pkg.__classifiers__

with open('README.md') as f:
    long_description = f.read()


try:
    reqs = open(os.path.join(os.path.dirname(__file__),
                             'requirements.txt')).read()
except (IOError, OSError):
    reqs = ''

setup(
    name=name,
    version=version,
    author=author,
    author_email=email,
    maintainer=maintainer,
    maintainer_email=maintainer_email,
    description='TheMovieDB.org APIv3 interface (Python 3.6+)',
    long_description=long_description,
    classifiers=classifiers,
    install_requires=reqs,
    packages=['tmdb3'],
    keywords='themoviedb.org',
)
