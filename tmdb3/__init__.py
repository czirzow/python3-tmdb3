#!/usr/bin/env python

from .tmdb_api import (
    Configuration, searchMovie, searchMovieWithYear,
    searchPerson, searchStudio, searchList, searchCollection,
    searchSeries, Person, Movie, Collection, Genre, List,
    Series, Studio, Network, Episode, Season)
from .request import set_key, set_cache
from .locales import get_locale, set_locale
from .tmdb_auth import get_session, set_session
from .cache_engine import CacheEngine
from .tmdb_exceptions import *

__title__ = ("tmdb_api - Simple-to-use Python interface to TMDB's API v3 "
             "(www.themoviedb.org)")

__author__ = 'Raymond Wagner <raymond@wagnerrp.com>'
__maintainer__ = 'Pol Canelles <canellestudi@gmail.com>'

__purpose__ = '''
This Python library is intended to provide a series of classes and methods
for search and retrieval of text metadata and image URLs from TMDB.
Preliminary API specifications can be found at
http://help.themoviedb.org/kb/api/about-3'''

__version__ = 'v0.7.2'

__classifiers__ = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries',
]
