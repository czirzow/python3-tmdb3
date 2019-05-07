# ----------------------------------------------
# Name:  TestCase for python3-tmdb3 tvshows api
# Author: Pol Canelles <canellestudi@gmail.com>
# Year: 2019
# License: Creative Commons GNU GPL v2
# (http://creativecommons.org/licenses/GPL/2.0/)
# ----------------------------------------------

import datetime
from httpretty import httprettified
from tmdb3.tmdb_api import (
    DiscoverTvSearchResult,
    SeriesSearchResult,
    Backdrop,
    Person,
    Genre,
    Poster,
    Network,
    Season,
)
from tmdb3 import discoverTv, searchSeries, Series
from tmdb3 import locales as tmdb3_locales

from tests import AbstractTestTmdbCase

tmdb3_locales.set_locale("en", "us", True)
tmdb3_locales.syslocale.encoding = "utf-8"

# dictionary to hold the data for our tv tests
test_tvshow_data = {
    "tvshow_discover": (
        "tv_discover_network_213.json",
        "{base_url}discover/tv?with_networks=213"
        "&first_air_date.gte=2019-03-30"
        "&first_air_date.lte=2019-04-30&api_key={api}",
    ),
    "tvshow_search": (
        "tv_search_star_wars.json",
        "{base_url}search/tv?query=Star+Wars&api_key={api}&language=en&page=1",
    ),
    "tvshow_info": (
        "tv_info_star_wars_clone_wars.json",
        "{base_url}tv/4194?language=en&api_key={api}",
    ),
    "tvshow_external_ids": (
        "tv_external_ids_star_wars_clone_wars.json",
        "{base_url}tv/4194/external_ids?api_key={api}",
    ),
    "tvshow_images": (
        "tv_images_star_wars_clone_wars.json",
        "{base_url}tv/4194/images?api_key={api}",
    ),
    "tvshow_similar": (
        "tv_similar_star_wars_clone_wars.json",
        "{base_url}tv/4194/similar?api_key={api}&language=en&page=1",
    ),
}


@httprettified
class TestTvshowSearch(AbstractTestTmdbCase):
    mock_data = test_tvshow_data
    mock_requests = ["tvshow_search"]

    def test_results_searchSeries(self):
        result = searchSeries("Star Wars")
        self.assertIsInstance(result, SeriesSearchResult)
        self.assertGreaterEqual(len(result), 18)


@httprettified
class TestTvshowDiscover(AbstractTestTmdbCase):
    mock_data = test_tvshow_data
    mock_requests = ["tvshow_discover"]

    def test_results_discoverSeries(self):
        result = discoverTv(
            with_networks="213",
            first_air_date_gte="2019-03-30",
            first_air_date_lte="2019-04-30",
        )
        self.assertIsInstance(result, DiscoverTvSearchResult)
        self.assertGreaterEqual(len(result), 23)
        self.assertIsInstance(result[0], Series)


@httprettified
class TestTvshow(AbstractTestTmdbCase):
    mock_data = test_tvshow_data
    mock_requests = [
        "tvshow_search",
        "tvshow_info",
        "tvshow_images",
        "tvshow_similar",
        "tvshow_external_ids",
    ]

    def test_serie(self):
        result = searchSeries("Star Wars")
        serie = [i for i in result if i.name == "Star Wars: The Clone Wars"][0]
        self.assertIsInstance(serie, Series)
        self.assertEqual(repr(serie), "<Series 'Star Wars: The Clone Wars'>")

        self.assertEqual(serie.name, "Star Wars: The Clone Wars")
        self.assertEqual(serie.original_name, "Star Wars: The Clone Wars")
        self.assertIsInstance(serie.origin_countries, list)
        self.assertEqual(serie.origin_countries[0], "SG")
        self.assertEqual(
            serie.overview,
            "Yoda, Obi-Wan Kenobi, Anakin Skywalker, Mace Windu "
            "and other Jedi Knights lead the Grand Army of the "
            "Republic against the droid army of the Separatists.",
        )

        self.assertEqual(serie.first_air_date, datetime.date(2008, 10, 3))
        self.assertEqual(serie.last_air_date, datetime.date(2014, 3, 7))

        self.assertIsInstance(serie.authors, list)
        self.assertIsInstance(serie.authors[0], Person)
        self.assertEqual(serie.authors[0].name, "George Lucas")

        self.assertEqual(serie.number_of_seasons, 6)
        self.assertEqual(serie.number_of_episodes, 121)
        self.assertEqual(serie.popularity, 31.739)
        self.assertEqual(serie.status, "Returning Series")
        self.assertEqual(serie.userrating, 7.5)
        self.assertEqual(serie.votes, 165)

        self.assertIsInstance(serie.genres, list)
        genre = serie.genres[0]
        self.assertIsInstance(genre, Genre)
        self.assertEqual(genre.id, 10759)
        self.assertEqual(genre.name, "Action & Adventure")

        self.assertIsInstance(serie.poster, Poster)
        self.assertTrue(serie.poster.geturl().startswith("http"))

        self.assertIsInstance(serie.backdrop, Backdrop)
        self.assertIsInstance(serie.backdrops, list)

        self.assertIsInstance(serie.networks, list)
        self.assertIsInstance(serie.networks[0], Network)

        self.assertIsInstance(serie.seasons, dict)
        self.assertIsInstance(serie.seasons[0], Season)

        self.assertEqual(serie.id, 4194)
        self.assertEqual(serie.imdb_id, "tt0458290")
        self.assertEqual(serie.tvdb_id, 83268)
        self.assertEqual(serie.tvrage_id, 19187)
        self.assertEqual(serie.freebase_id, "")
        self.assertEqual(serie.freebase_mid, "/m/02q70n3")

        similars = serie.getSimilar()
        self.assertIsInstance(similars, SeriesSearchResult)
        first_similar = similars[0]
        self.assertIsInstance(first_similar, Series)
        self.assertEqual(first_similar.name, "Star Wars Rebels")
