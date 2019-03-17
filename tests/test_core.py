# ----------------------------------------------
# Name:  TestCase for python3-tmdb3 core modules
# Author: Pol Canelles <canellestudi@gmail.com>
# Year: 2019
# License: Creative Commons GNU GPL v2
# (http://creativecommons.org/licenses/GPL/2.0/)
# ----------------------------------------------

from os.path import join, dirname, isfile
from os import remove
from httpretty import httprettified

from tests import AbstractTestTmdbCase
from tests.test_movies_api import test_movie_data

from tmdb3 import locales as tmdb3_locales
from tmdb3 import searchMovie
from tmdb3.tmdb_exceptions import TMDBCacheError
from tmdb3.tmdb_api import MovieSearchResult
from tmdb3.cache import Cache
from tmdb3.cache_file import FileEngine

tmdb3_locales.set_locale("en", "us", True)
tmdb3_locales.syslocale.encoding = 'utf-8'

CACHE_FILE = join(dirname(__file__), 'tmdb3.cache')
# Remove any cache file that we could have from a failed test
if isfile(CACHE_FILE):
    remove(CACHE_FILE)


@httprettified
class TestCache(AbstractTestTmdbCase):
    mock_data = test_movie_data
    mock_requests = ['movie_search', 'movie_info']
    cache_file = CACHE_FILE

    def tearDown(self):
        if isfile(self.cache_file):
            remove(self.cache_file)

    def test_cache_configure(self):
        cache = Cache(filename=self.cache_file)
        self.assertIsInstance(cache._engine, FileEngine)
        self.assertRaises(TMDBCacheError, cache.configure, 'fake-engine')

    def test_read_write_cache(self):
        # The cache file should not exist at this point
        self.assertFalse(isfile(self.cache_file))
        # Perform a query, so we force to create the cache file
        result = searchMovie('Star Wars', year=1977)
        self.assertIsInstance(result, MovieSearchResult)
        # The cache file should be created at this point
        self.assertTrue(isfile(self.cache_file))
        # Here we test the reading of the cache file by requesting some info
        movie = [i for i in result if i.title == 'Star Wars'][0]
        self.assertEqual(movie.imdb, 'tt0076759')
