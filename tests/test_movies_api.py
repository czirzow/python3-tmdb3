# ----------------------------------------------
# Name:  TestCase for python3-tmdb3 movies api
# Author: Pol Canelles <canellestudi@gmail.com>
# Year: 2019
# License: Creative Commons GNU GPL v2
# (http://creativecommons.org/licenses/GPL/2.0/)
# ----------------------------------------------

from httpretty import httprettified
from datetime import date

from tmdb3.tmdb_api import (
    MovieSearchResult,
    AppleTrailer,
    Backdrop,
    Genre,
    Poster,
    Studio,
)
from tmdb3 import (
    searchMovie,
    searchMovieWithYear,
    Collection,
    Movie,
)
from tmdb3.tmdb_exceptions import TMDBImageSizeError
from tmdb3 import locales as tmdb3_locales
from tests import AbstractTestTmdbCase

tmdb3_locales.set_locale("en", "us", True)
tmdb3_locales.syslocale.encoding = 'utf-8'

# dictionary to hold the data for our movies tests
test_movie_data = {
    'movie_search': (
        'movie_search_star_wars_1977.json',
        ('{base_url}search/movie?query=Star+Wars&include_adult=False'
         '&year=1977&api_key={api}&language=en&page=1')
    ),
    'movie_info': (
        'movie_info_star_wars_1977.json',
        '{base_url}movie/11?language=en&api_key={api}'
    ),
    'movie_tmdb_config': (
        'movie_tmdb_configuration.json',
        '{base_url}configuration?api_key={api}'
    ),
    'movie_images': (
        'movie_images_star_wars_1977.json',
        '{base_url}movie/11/images?api_key={api}'
    ),
    'movie_trailers': (
        'movie_trailers_star_wars_1977.json',
        '{base_url}movie/11/trailers?language=en&api_key={api}'
    ),
    'movie_similar': (
        'movie_similar_star_wars_1977.json',
        '{base_url}movie/11/similar_movies?api_key={api}&language=en&page=1'
    ),
}


@httprettified
class TestMoviesSearch(AbstractTestTmdbCase):
    mock_data = test_movie_data
    mock_requests = ['movie_search']

    def test_searchMovie(self):
        result = searchMovie('Star Wars', year=1977)
        self.assertIsInstance(result, MovieSearchResult)
        self.assertGreaterEqual(len(result), 2)

    def test_searchMovieWithYear(self):
        result = searchMovieWithYear('{} ({})'.format('Star Wars', 1977))
        self.assertIsInstance(result, MovieSearchResult)
        self.assertGreaterEqual(len(result), 2)


@httprettified
class TestMovie(AbstractTestTmdbCase):
    mock_data = test_movie_data
    mock_requests = [
        'movie_search',
        'movie_info',
        'movie_tmdb_config',
        'movie_images',
        'movie_trailers',
        'movie_similar',
    ]

    def test_movie(self):
        result = searchMovie('Star Wars', year=1977)
        movie = [i for i in result if i.title == 'Star Wars'][0]
        self.assertIsInstance(movie, Movie)
        self.assertEqual(repr(movie), "<Movie 'Star Wars' (1977)>")

        self.assertEqual(movie.id, 11)
        self.assertEqual(movie.imdb, 'tt0076759')
        self.assertEqual(movie.title, 'Star Wars')
        self.assertEqual(movie.originaltitle, 'Star Wars')
        self.assertEqual(movie.tagline,
                         'A long time ago in a galaxy far, far away...')
        self.assertEqual(movie.overview,
                         'Princess Leia is captured and held hostage by the '
                         'evil Imperial forces in their effort to take over '
                         'the galactic Empire. Venturesome Luke Skywalker and '
                         'dashing captain Han Solo team together with the '
                         'loveable robot duo R2-D2 and C-3PO to rescue the '
                         'beautiful princess and restore peace and justice in '
                         'the Empire.')
        self.assertEqual(movie.budget, 11000000)
        self.assertGreaterEqual(movie.revenue, 775398007)
        self.assertEqual(movie.releasedate, date(1977, 5, 25))
        self.assertEqual(movie.homepage, 'http://www.starwars.com/films/'
                                         'star-wars-episode-iv-a-new-hope')
        self.assertIsInstance(movie.popularity, float)
        self.assertIsInstance(movie.userrating, float)
        self.assertIsInstance(movie.votes, int)
        self.assertFalse(movie.adult)
        self.assertIsInstance(movie.countries, list)
        self.assertIsInstance(movie.languages, list)

        self.assertIsInstance(movie.poster, Poster)
        self.assertTrue(movie.poster.geturl().startswith('http'))
        self.assertEqual(
            movie.poster.sizes(),
            ['w92', 'w154', 'w185', 'w342', 'w500', 'w780', 'original']
        )
        self.assertRaises(TMDBImageSizeError, movie.poster.geturl, 'wrong')

        self.assertIsInstance(movie.poster.sizes(), list)
        self.assertGreater(len(movie.poster.sizes()), 1)
        self.assertIsInstance(movie.posters, list)
        self.assertIsInstance(movie.posters[0], Poster)

        self.assertIsInstance(movie.genres, list)
        genre = movie.genres[0]
        self.assertIsInstance(genre, Genre)
        self.assertEqual(genre.id, 12)
        self.assertEqual(genre.name, 'Adventure')

        self.assertIsInstance(movie.apple_trailers, list)

        self.assertIsInstance(movie.backdrop, Backdrop)
        self.assertIsInstance(movie.backdrops, list)
        self.assertIsInstance(movie.collection, Collection)

        self.assertIsInstance(movie.studios, list)
        self.assertIsInstance(movie.studios[0], Studio)

        self.assertIsInstance(movie.similar, MovieSearchResult)
