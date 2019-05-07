#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------
# Name: tmdb_api.py    Simple-to-use Python interface to TMDB's API v3
# Python Library
# Author: Raymond Wagner
# Purpose: This Python library is intended to provide a series of classes
#          and methods for search and retrieval of text metadata and image
#          URLs from TMDB.
#          Preliminary API specifications can be found at
#          http://help.themoviedb.org/kb/api/about-3
# License: Creative Commons GNU GPL v2
# (http://creativecommons.org/licenses/GPL/2.0/)
# -----------------------

import datetime

from .request import set_key, Request
from .util import Datapoint, Datalist, Datadict, Element, NameRepr, SearchRepr
from .pager import PagedRequest
from .locales import get_locale, set_locale
from .tmdb_auth import get_session, set_session
from .tmdb_exceptions import *

DEBUG = False


def process_date(datestr):
    try:
        return datetime.date(*[int(x) for x in datestr.split("-")])
    except (TypeError, ValueError):
        import sys
        import warnings
        import traceback

        _, _, tb = sys.exc_info()
        f, l, _, _ = traceback.extract_tb(tb)[-1]
        warnings.warn_explicit(
            f'"{datestr}" is not a supported date format. '
            f"Please fix upstream data at "
            f"http://www.themoviedb.org.",
            Warning,
            f,
            l,
        )
        return None


class Configuration(Element):
    images = Datapoint("images")

    def _populate(self):
        return Request("configuration")


Configuration = Configuration()


class Account(NameRepr, Element):
    def _populate(self):
        return Request("account", session_id=self._session.sessionid)

    id = Datapoint("id")
    adult = Datapoint("include_adult")
    country = Datapoint("iso_3166_1")
    language = Datapoint("iso_639_1")
    name = Datapoint("name")
    username = Datapoint("username")

    @property
    def locale(self):
        return get_locale(self.language, self.country)


def discoverTv(
    sort_by=None,
    first_air_date_year=None,
    with_genres=None,
    with_networks=None,
    without_genres=None,
    without_keywords=None,
    air_date_gte=None,
    ir_date_lte=None,
    first_air_date_gte=None,
    first_air_date_lte=None,
    vote_average_gte=None,
    vote_count_gte=None,
    with_runtime_gte=None,
    with_runtime_lte=None,
    locale=None,
):
    return DiscoverTvSearchResult(
        Request(
            "discover/tv",
            sort_by=sort_by,
            first_air_date_year=first_air_date_year,
            with_genres=with_genres,
            with_networks=with_networks,
            without_genres=without_genres,
            without_keywords=without_keywords,
            air_date_gte=air_date_gte,
            ir_date_lte=ir_date_lte,
            first_air_date_gte=first_air_date_gte,
            first_air_date_lte=first_air_date_lte,
            vote_average_gte=vote_average_gte,
            vote_count_gte=vote_count_gte,
            with_runtime_gte=with_runtime_gte,
            with_runtime_lte=with_runtime_lte,
        ),
        locale=locale,
    )


class DiscoverTvSearchResult(SearchRepr, PagedRequest):
    """Stores a list of search matches."""

    _name = "Discover Tv"

    def __init__(self, request, locale=None):
        if locale is None:
            locale = get_locale()
        super(DiscoverTvSearchResult, self).__init__(
            request.new(language=locale.language),
            lambda x: Series(raw=x, locale=locale),
        )


def discoverMovie(
    sort_by=None,
    with_cast=None,
    with_crew=None,
    with_genres=None,
    without_genres=None,
    with_companies=None,
    with_keywords=None,
    without_keywords=None,
    include_adult=None,
    year=None,
    region=None,
    primary_release_year=None,
    primary_release_date_gte=None,
    primary_release_date_lte=None,
    release_date_gte=None,
    release_date_lte=None,
    vote_average_gte=None,
    vote_average_lte=None,
    vote_count_gte=None,
    vote_count_lte=None,
    with_runtime_gte=None,
    with_runtime_lte=None,
    with_release_type=None,
    with_original_language=None,
    locale=None,
):
    return DiscoverMovieSearchResult(
        Request(
            "discover/movie",
            sort_by=sort_by,
            with_cast=with_cast,
            with_crew=with_crew,
            with_genres=with_genres,
            without_genres=without_genres,
            with_companies=with_companies,
            with_keywords=with_keywords,
            without_keywords=without_keywords,
            include_adult=include_adult,
            year=year,
            region=region,
            primary_release_year=primary_release_year,
            primary_release_date_gte=primary_release_date_gte,
            primary_release_date_lte=primary_release_date_lte,
            release_date_gte=release_date_gte,
            release_date_lte=release_date_lte,
            vote_average_gte=vote_average_gte,
            vote_average_lte=vote_average_lte,
            vote_count_gte=vote_count_gte,
            vote_count_lte=vote_count_lte,
            with_runtime_gte=with_runtime_gte,
            with_runtime_lte=with_runtime_lte,
            with_release_type=with_release_type,
            with_original_language=with_original_language,
        ),
        locale=locale,
    )


class DiscoverMovieSearchResult(SearchRepr, PagedRequest):
    """Stores a list of search matches."""

    _name = "Discover Movie"

    def __init__(self, request, locale=None):
        if locale is None:
            locale = get_locale()
        super(DiscoverMovieSearchResult, self).__init__(
            request.new(language=locale.language),
            lambda x: Movie(raw=x, locale=locale),
        )


def searchMovie(query, locale=None, adult=False, year=None):
    kwargs = {"query": query, "include_adult": adult}
    if year is not None:
        try:
            kwargs["year"] = year.year
        except AttributeError:
            kwargs["year"] = year
    return MovieSearchResult(Request("search/movie", **kwargs), locale=locale)


def searchMovieWithYear(query, locale=None, adult=False):
    year = None
    if (len(query) > 6) and (query[-1] == ")") and (query[-6] == "("):
        # simple syntax check, no need for regular expression
        try:
            year = int(query[-5:-1])
        except ValueError:
            pass
        else:
            if 1885 < year < 2050:
                # strip out year from search
                query = query[:-7]
            else:
                # sanity check on resolved year failed, pass through
                year = None
    return searchMovie(query, locale, adult, year)


class MovieSearchResult(SearchRepr, PagedRequest):
    """Stores a list of search matches."""

    _name = None

    def __init__(self, request, locale=None):
        if locale is None:
            locale = get_locale()
        super(MovieSearchResult, self).__init__(
            request.new(language=locale.language),
            lambda x: Movie(raw=x, locale=locale),
        )


def searchSeries(
    query, first_air_date_year=None, search_type=None, locale=None
):
    return SeriesSearchResult(
        Request(
            "search/tv",
            query=query,
            first_air_date_year=first_air_date_year,
            search_type=search_type,
        ),
        locale=locale,
    )


class SeriesSearchResult(SearchRepr, PagedRequest):
    """Stores a list of search matches."""

    _name = None

    def __init__(self, request, locale=None):
        if locale is None:
            locale = get_locale()
        super(SeriesSearchResult, self).__init__(
            request.new(language=locale.language),
            lambda x: Series(raw=x, locale=locale),
        )


def searchPerson(query, adult=False):
    return PeopleSearchResult(
        Request("search/person", query=query, include_adult=adult)
    )


class PeopleSearchResult(SearchRepr, PagedRequest):
    """Stores a list of search matches."""

    _name = None

    def __init__(self, request):
        super(PeopleSearchResult, self).__init__(
            request, lambda x: Person(raw=x)
        )


def searchStudio(query):
    return StudioSearchResult(Request("search/company", query=query))


class StudioSearchResult(SearchRepr, PagedRequest):
    """Stores a list of search matches."""

    _name = None

    def __init__(self, request):
        super(StudioSearchResult, self).__init__(
            request, lambda x: Studio(raw=x)
        )


def searchList(query, adult=False):
    ListSearchResult(Request("search/list", query=query, include_adult=adult))


class ListSearchResult(SearchRepr, PagedRequest):
    """Stores a list of search matches."""

    _name = None

    def __init__(self, request):
        super(ListSearchResult, self).__init__(request, lambda x: List(raw=x))


def searchCollection(query, locale=None):
    return CollectionSearchResult(
        Request("search/collection", query=query), locale=locale
    )


class CollectionSearchResult(SearchRepr, PagedRequest):
    """Stores a list of search matches."""

    _name = None

    def __init__(self, request, locale=None):
        if locale is None:
            locale = get_locale()
        super(CollectionSearchResult, self).__init__(
            request.new(language=locale.language),
            lambda x: Collection(raw=x, locale=locale),
        )


class Image(Element):
    filename = Datapoint(
        "file_path", initarg=1, handler=lambda x: x.lstrip("/")
    )
    aspectratio = Datapoint("aspect_ratio")
    height = Datapoint("height")
    width = Datapoint("width")
    language = Datapoint("iso_639_1")
    userrating = Datapoint("vote_average")
    votes = Datapoint("vote_count")

    def sizes(self):
        return ["original"]

    def geturl(self, size="original"):
        if size not in self.sizes():
            raise TMDBImageSizeError
        url = Configuration.images["base_url"].rstrip("/")
        return f"{url}/{size}/{self.filename}"

    # sort preferring locale's language, but keep remaining ordering consistent
    def __lt__(self, other):
        if not isinstance(other, Image):
            return False
        return (self.language == self._locale.language) and (
            self.language != other.language
        )

    def __gt__(self, other):
        if not isinstance(other, Image):
            return True
        return (self.language != other.language) and (
            other.language == self._locale.language
        )

    # direct match for comparison
    def __eq__(self, other):
        if not isinstance(other, Image):
            return False
        return self.filename == other.filename

    # special handling for boolean to see if exists
    def __bool__(self):
        if len(self.filename) == 0:
            return False
        return True

    def __repr__(self):
        # BASE62 encoded filename, no need to worry about unicode
        return f"<{self.__class__.__name__} '{self.filename}'>"


class Backdrop(Image):
    def sizes(self):
        return Configuration.images["backdrop_sizes"]


class Poster(Image):
    def sizes(self):
        return Configuration.images["poster_sizes"]


class Profile(Image):
    def sizes(self):
        return Configuration.images["profile_sizes"]


class Logo(Image):
    def sizes(self):
        return Configuration.images["logo_sizes"]


class AlternateTitle(Element):
    country = Datapoint("iso_3166_1")
    title = Datapoint("title")

    # sort preferring locale's country, but keep remaining ordering consistent
    def __lt__(self, other):
        return (self.country == self._locale.country) and (
            self.country != other.country
        )

    def __gt__(self, other):
        return (self.country != other.country) and (
            other.country == self._locale.country
        )

    def __eq__(self, other):
        return self.country == other.country

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.title}' ({self.country})>"


class Person(Element):
    id = Datapoint("id", initarg=1)
    name = Datapoint("name")
    biography = Datapoint("biography")
    dayofbirth = Datapoint("birthday", default=None, handler=process_date)
    dayofdeath = Datapoint("deathday", default=None, handler=process_date)
    homepage = Datapoint("homepage")
    birthplace = Datapoint("place_of_birth")
    profile = Datapoint(
        "profile_path", handler=Profile, raw=False, default=None
    )
    adult = Datapoint("adult")
    aliases = Datalist("also_known_as")

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.name}'>"

    def _populate(self):
        return Request(f"person/{self.id}")

    def _populate_credits(self):
        return Request(
            f"person/{self.id}/credits", language=self._locale.language
        )

    def _populate_images(self):
        return Request(f"person/{self.id}/images")

    roles = Datalist(
        "cast", handler=lambda x: ReverseCast(raw=x), poller=_populate_credits
    )
    crew = Datalist(
        "crew", handler=lambda x: ReverseCrew(raw=x), poller=_populate_credits
    )
    profiles = Datalist("profiles", handler=Profile, poller=_populate_images)


class Cast(Person):
    character = Datapoint("character")
    order = Datapoint("order")

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} '{self.name}' as '{self.character}'>"
        )


class Crew(Person):
    job = Datapoint("job")
    department = Datapoint("department")

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.name}','{self.job}'>"


class Keyword(Element):
    id = Datapoint("id")
    name = Datapoint("name")

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.name}'>"


class Release(Element):
    certification = Datapoint("certification")
    country = Datapoint("iso_3166_1")
    releasedate = Datapoint("release_date", handler=process_date)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} '{self.country}', {self.releasedate}>"
        )


class Trailer(Element):
    name = Datapoint("name")
    size = Datapoint("size")
    source = Datapoint("source")


class YoutubeTrailer(Trailer):
    def geturl(self):
        self.source = self.source.encode("ascii", errors="ignore")
        return f"http://www.youtube.com/watch?v={self.source}"

    def __repr__(self):
        # modified BASE64 encoding, no need to worry about unicode
        return f"<{self.__class__.__name__} '{self.name}'>"


class AppleTrailer(Element):
    name = Datapoint("name")
    sources = Datadict("sources", handler=Trailer, attr="size")

    def sizes(self):
        return list(self.sources.keys())

    def geturl(self, size=None):
        if size is None:
            # sort assuming ###p format for now, take largest resolution
            size = (
                str(sorted([int(size[:-1]) for size in self.sources])[-1])
                + "p"
            )
        return self.sources[size].source

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.name}'>"


class Translation(Element):
    name = Datapoint("name")
    language = Datapoint("iso_639_1")
    englishname = Datapoint("english_name")

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.name}' ({self.language})>"


class Genre(NameRepr, Element):
    id = Datapoint("id")
    name = Datapoint("name")

    def _populate_movies(self):
        return Request(
            f"genre/{self.id}/movies", language=self._locale.language
        )

    @property
    def movies(self):
        if "movies" not in self._data:
            search = MovieSearchResult(
                self._populate_movies(), locale=self._locale
            )
            search._name = "{0.name} Movies".format(self)
            self._data["movies"] = search
        return self._data["movies"]

    @classmethod
    def getAll(cls, locale=None):
        class GenreList(Element):
            genres = Datalist("genres", handler=Genre)

            def _populate(self):
                return Request("genre/list", language=self._locale.language)

        return GenreList(locale=locale).genres


class Studio(NameRepr, Element):
    id = Datapoint("id", initarg=1)
    name = Datapoint("name")
    description = Datapoint("description")
    headquarters = Datapoint("headquarters")
    logo = Datapoint("logo_path", handler=Logo, raw=False, default=None)
    # FIXME: manage not-yet-defined handlers in a way that will propogate
    #        locale information properly
    parent = Datapoint("parent_company", handler=lambda x: Studio(raw=x))

    def _populate(self):
        return Request("company/{0}".format(self.id))

    def _populate_movies(self):
        return Request(
            "company/{0}/movies".format(self.id),
            language=self._locale.language,
        )

    # FIXME: add a cleaner way of adding types with no additional processing
    @property
    def movies(self):
        if "movies" not in self._data:
            search = MovieSearchResult(
                self._populate_movies(), locale=self._locale
            )
            search._name = f"{self.id.name} Movies"
            self._data["movies"] = search
        return self._data["movies"]


class Country(NameRepr, Element):
    code = Datapoint("iso_3166_1")
    name = Datapoint("name")


class Language(NameRepr, Element):
    code = Datapoint("iso_639_1")
    name = Datapoint("name")


class Movie(Element):
    @classmethod
    def latest(cls):
        req = Request("latest/movie")
        req.lifetime = 600
        return cls(raw=req.readJSON())

    @classmethod
    def nowplaying(cls, locale=None):
        res = MovieSearchResult(Request("movie/now-playing"), locale=locale)
        res._name = "Now Playing"
        return res

    @classmethod
    def mostpopular(cls, locale=None):
        res = MovieSearchResult(Request("movie/popular"), locale=locale)
        res._name = "Popular"
        return res

    @classmethod
    def toprated(cls, locale=None):
        res = MovieSearchResult(Request("movie/top_rated"), locale=locale)
        res._name = "Top Rated"
        return res

    @classmethod
    def upcoming(cls, locale=None):
        res = MovieSearchResult(Request("movie/upcoming"), locale=locale)
        res._name = "Upcoming"
        return res

    @classmethod
    def favorites(cls, session=None):
        if session is None:
            session = get_session()
        account = Account(session=session)
        res = MovieSearchResult(
            Request(
                f"account/{account.id}/favorite_movies",
                session_id=session.sessionid,
            )
        )
        res._name = "Favorites"
        return res

    @classmethod
    def ratedmovies(cls, session=None):
        if session is None:
            session = get_session()
        account = Account(session=session)
        res = MovieSearchResult(
            Request(
                f"account/{account.id}/rated_movies",
                session_id=session.sessionid,
            )
        )
        res._name = "Movies You Rated"
        return res

    @classmethod
    def watchlist(cls, session=None):
        if session is None:
            session = get_session()
        account = Account(session=session)
        res = MovieSearchResult(
            Request(
                f"account/{account.id}/movie_watchlist",
                session_id=session.sessionid,
            )
        )
        res._name = "Movies You're Watching"
        return res

    @classmethod
    def fromIMDB(cls, imdbid, locale=None):
        try:
            # assume string
            if not imdbid.startswith("tt"):
                imdbid = f"tt{imdbid:0>7}"
        except AttributeError:
            # assume integer
            imdbid = f"tt{imdbid:0>7}"
        if locale is None:
            locale = get_locale()
        movie = cls(imdbid, locale=locale)
        movie._populate()
        return movie

    id = Datapoint("id", initarg=1)
    title = Datapoint("title")
    originaltitle = Datapoint("original_title")
    tagline = Datapoint("tagline")
    overview = Datapoint("overview")
    runtime = Datapoint("runtime")
    budget = Datapoint("budget")
    revenue = Datapoint("revenue")
    releasedate = Datapoint("release_date", handler=process_date)
    homepage = Datapoint("homepage")
    imdb = Datapoint("imdb_id")

    backdrop = Datapoint(
        "backdrop_path", handler=Backdrop, raw=False, default=None
    )
    poster = Datapoint("poster_path", handler=Poster, raw=False, default=None)

    popularity = Datapoint("popularity")
    userrating = Datapoint("vote_average")
    votes = Datapoint("vote_count")

    adult = Datapoint("adult")
    collection = Datapoint(
        "belongs_to_collection", handler=lambda x: Collection(raw=x)
    )
    genres = Datalist("genres", handler=Genre)
    studios = Datalist("production_companies", handler=Studio)
    countries = Datalist("production_countries", handler=Country)
    languages = Datalist("spoken_languages", handler=Language)

    def _populate(self):
        return Request(f"movie/{self.id}", language=self._locale.language)

    def _populate_titles(self):
        kwargs = {}
        if not self._locale.fallthrough:
            kwargs["country"] = self._locale.country
        return Request(f"movie/{self.id}/alternative_titles", **kwargs)

    def _populate_cast(self):
        return Request("movie/{0}/casts".format(self.id))

    def _populate_images(self):
        kwargs = {}
        if not self._locale.fallthrough:
            kwargs["language"] = self._locale.language
        return Request(f"movie/{self.id}/images", **kwargs)

    def _populate_keywords(self):
        return Request(f"movie/{self.id}/keywords")

    def _populate_releases(self):
        return Request(f"movie/{self.id}/releases")

    def _populate_trailers(self):
        return Request(
            f"movie/{self.id}/trailers", language=self._locale.language
        )

    def _populate_translations(self):
        return Request(f"movie/{self.id}/translations")

    alternate_titles = Datalist(
        "titles", handler=AlternateTitle, poller=_populate_titles, sort=True
    )

    # FIXME: this data point will need to be changed to 'credits' at some point
    cast = Datalist("cast", handler=Cast, poller=_populate_cast, sort="order")

    crew = Datalist("crew", handler=Crew, poller=_populate_cast)
    backdrops = Datalist(
        "backdrops", handler=Backdrop, poller=_populate_images, sort=True
    )
    posters = Datalist(
        "posters", handler=Poster, poller=_populate_images, sort=True
    )
    keywords = Datalist("keywords", handler=Keyword, poller=_populate_keywords)
    releases = Datadict(
        "countries", handler=Release, poller=_populate_releases, attr="country"
    )
    youtube_trailers = Datalist(
        "youtube", handler=YoutubeTrailer, poller=_populate_trailers
    )
    apple_trailers = Datalist(
        "quicktime", handler=AppleTrailer, poller=_populate_trailers
    )
    translations = Datalist(
        "translations", handler=Translation, poller=_populate_translations
    )

    def setFavorite(self, value):
        req = Request(
            "account/{0}/favorite".format(Account(session=self._session).id),
            session_id=self._session.sessionid,
        )
        req.add_data(
            {"movie_id": self.id, "favorite": str(bool(value)).lower()}
        )
        req.lifetime = 0
        req.readJSON()

    def setRating(self, value):
        if not (0 <= value <= 10):
            raise TMDBError("Ratings must be between '0' and '10'.")
        req = Request(
            f"movie/{self.id}/rating", session_id=self._session.sessionid
        )
        req.lifetime = 0
        req.add_data({"value": value})
        req.readJSON()

    def setWatchlist(self, value):
        req = Request(
            f"account/{Account(session=self._session).id}/movie_watchlist",
            session_id=self._session.sessionid,
        )
        req.lifetime = 0
        req.add_data(
            {"movie_id": self.id, "movie_watchlist": str(bool(value)).lower()}
        )
        req.readJSON()

    def getSimilar(self):
        return self.similar

    @property
    def similar(self):
        res = MovieSearchResult(
            Request(f"movie/{self.id}/similar_movies"), locale=self._locale
        )
        res._name = f"Similar to {self._printable_name()}"
        return res

    @property
    def lists(self):
        res = ListSearchResult(Request(f"movie/{self.id}/lists"))
        res._name = "Lists containing {0}".format(self._printable_name())
        return res

    def _printable_name(self):
        if self.title is not None:
            s = f"'{self.title}'"
        elif self.originaltitle is not None:
            s = f"'{self.originaltitle}'"
        else:
            s = "'No Title'"
        if self.releasedate:
            s = f"{s} ({self.releasedate.year})"
        return s

    def __repr__(self):
        return f"<{self.__class__.__name__} {self._printable_name()}>"


class ReverseCast(Movie):
    character = Datapoint("character")

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} '{self.character}' "
            f"on {self._printable_name()}>"
        )


class ReverseCrew(Movie):
    department = Datapoint("department")
    job = Datapoint("job")

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} '{self.job}' "
            f"for {self._printable_name()}>"
        )


class Collection(NameRepr, Element):
    id = Datapoint("id", initarg=1)
    name = Datapoint("name")
    backdrop = Datapoint(
        "backdrop_path", handler=Backdrop, raw=False, default=None
    )
    poster = Datapoint("poster_path", handler=Poster, raw=False, default=None)
    members = Datalist("parts", handler=Movie)
    overview = Datapoint("overview")

    def _populate(self):
        return Request(f"collection/{self.id}", language=self._locale.language)

    def _populate_images(self):
        kwargs = {}
        if not self._locale.fallthrough:
            kwargs["language"] = self._locale.language
        return Request(f"collection/{self.id}/images", **kwargs)

    backdrops = Datalist(
        "backdrops", handler=Backdrop, poller=_populate_images, sort=True
    )
    posters = Datalist(
        "posters", handler=Poster, poller=_populate_images, sort=True
    )


class List(NameRepr, Element):
    id = Datapoint("id", initarg=1)
    name = Datapoint("name")
    author = Datapoint("created_by")
    description = Datapoint("description")
    favorites = Datapoint("favorite_count")
    language = Datapoint("iso_639_1")
    count = Datapoint("item_count")
    poster = Datapoint("poster_path", handler=Poster, raw=False, default=None)
    members = Datalist("items", handler=Movie)

    def _populate(self):
        return Request(f"list/{self.id}")


class Network(NameRepr, Element):
    id = Datapoint("id", initarg=1)
    name = Datapoint("name")


class Episode(NameRepr, Element):
    episode_number = Datapoint("episode_number", initarg=3)
    season_number = Datapoint("season_number", initarg=2)
    series_id = Datapoint("series_id", initarg=1)
    air_date = Datapoint("air_date", handler=process_date)
    overview = Datapoint("overview")
    name = Datapoint("name")
    userrating = Datapoint("vote_average")
    votes = Datapoint("vote_count")
    id = Datapoint("id")
    production_code = Datapoint("production_code")
    still = Datapoint("still_path", handler=Backdrop, raw=False, default=None)

    def _populate(self):
        return Request(
            f"tv/{self.series_id}/"
            f"season/{self.season_number}/"
            f"episode/{self.episode_number}",
            language=self._locale.language,
        )

    def _populate_cast(self):
        return Request(
            f"tv/{self.series_id}/"
            f"season/{self.season_number}/"
            f"episode/{self.episode_number}/credits",
            language=self._locale.language,
        )

    def _populate_external_ids(self):
        return Request(
            f"tv/{self.series_id}/season/{self.season_number}/"
            f"episode/{self.episode_number}/external_ids"
        )

    def _populate_images(self):
        kwargs = {}
        if not self._locale.fallthrough:
            kwargs["language"] = self._locale.language
        return Request(
            f"tv/{self.series_id}/season/{self.season_number}/"
            f"episode/{self.episode_number}/images",
            **kwargs,
        )

    cast = Datalist("cast", handler=Cast, poller=_populate_cast, sort="order")
    guest_stars = Datalist(
        "guest_stars", handler=Cast, poller=_populate_cast, sort="order"
    )
    crew = Datalist("crew", handler=Crew, poller=_populate_cast)
    imdb_id = Datapoint("imdb_id", poller=_populate_external_ids)
    freebase_id = Datapoint("freebase_id", poller=_populate_external_ids)
    freebase_mid = Datapoint("freebase_mid", poller=_populate_external_ids)
    tvdb_id = Datapoint("tvdb_id", poller=_populate_external_ids)
    tvrage_id = Datapoint("tvrage_id", poller=_populate_external_ids)
    stills = Datalist(
        "stills", handler=Backdrop, poller=_populate_images, sort=True
    )


class Season(NameRepr, Element):
    season_number = Datapoint("season_number", initarg=2)
    series_id = Datapoint("series_id", initarg=1)
    id = Datapoint("id")
    air_date = Datapoint("air_date", handler=process_date)
    poster = Datapoint("poster_path", handler=Poster, raw=False, default=None)
    overview = Datapoint("overview")
    name = Datapoint("name")
    episodes = Datadict(
        "episodes",
        attr="episode_number",
        handler=Episode,
        passthrough={
            "series_id": "series_id",
            "season_number": "season_number",
        },
    )

    def _populate(self):
        return Request(
            f"tv/{self.series_id}/season/{self.season_number}",
            language=self._locale.language,
        )

    def _populate_images(self):
        kwargs = {}
        if not self._locale.fallthrough:
            kwargs["language"] = self._locale.language
        return Request(
            f"tv/{self.series_id}/" f"season/{self.season_number}/images",
            **kwargs,
        )

    def _populate_external_ids(self):
        return Request(
            f"tv/{self.series_id}/season/{self.season_number}/external_ids"
        )

    posters = Datalist(
        "posters", handler=Poster, poller=_populate_images, sort=True
    )

    freebase_id = Datapoint("freebase_id", poller=_populate_external_ids)
    freebase_mid = Datapoint("freebase_mid", poller=_populate_external_ids)
    tvdb_id = Datapoint("tvdb_id", poller=_populate_external_ids)
    tvrage_id = Datapoint("tvrage_id", poller=_populate_external_ids)


class Series(NameRepr, Element):
    id = Datapoint("id", initarg=1)
    backdrop = Datapoint(
        "backdrop_path", handler=Backdrop, raw=False, default=None
    )
    authors = Datalist("created_by", handler=Person)
    episode_run_times = Datalist("episode_run_time")
    first_air_date = Datapoint("first_air_date", handler=process_date)
    last_air_date = Datapoint("last_air_date", handler=process_date)
    genres = Datalist("genres", handler=Genre)
    homepage = Datapoint("homepage")
    in_production = Datapoint("in_production")
    languages = Datalist("languages")
    origin_countries = Datalist("origin_country")
    name = Datapoint("name")
    original_name = Datapoint("original_name")
    number_of_episodes = Datapoint("number_of_episodes")
    number_of_seasons = Datapoint("number_of_seasons")
    overview = Datapoint("overview")
    popularity = Datapoint("popularity")
    status = Datapoint("status")
    userrating = Datapoint("vote_average")
    votes = Datapoint("vote_count")
    poster = Datapoint("poster_path", handler=Poster, raw=False, default=None)
    networks = Datalist("networks", handler=Network)
    seasons = Datadict(
        "seasons",
        attr="season_number",
        handler=Season,
        passthrough={"id": "series_id"},
    )

    def _populate(self):
        return Request(f"tv/{self.id}", language=self._locale.language)

    def _populate_cast(self):
        return Request(f"tv/{self.id}/credits")

    def _populate_images(self):
        kwargs = {}
        if not self._locale.fallthrough:
            kwargs["language"] = self._locale.language
        return Request(f"tv/{self.id}/images", **kwargs)

    def _populate_external_ids(self):
        return Request(f"tv/{self.id}/external_ids")

    def _populate_keywords(self):
        return Request(f"tv/{self.id}/keywords")

    cast = Datalist("cast", handler=Cast, poller=_populate_cast, sort="order")
    crew = Datalist("crew", handler=Crew, poller=_populate_cast)
    backdrops = Datalist(
        "backdrops", handler=Backdrop, poller=_populate_images, sort=True
    )
    posters = Datalist(
        "posters", handler=Poster, poller=_populate_images, sort=True
    )
    keywords = Datalist("results", handler=Keyword, poller=_populate_keywords)

    imdb_id = Datapoint("imdb_id", poller=_populate_external_ids)
    freebase_id = Datapoint("freebase_id", poller=_populate_external_ids)
    freebase_mid = Datapoint("freebase_mid", poller=_populate_external_ids)
    tvdb_id = Datapoint("tvdb_id", poller=_populate_external_ids)
    tvrage_id = Datapoint("tvrage_id", poller=_populate_external_ids)

    def getSimilar(self):
        return self.similar

    @property
    def similar(self):
        res = SeriesSearchResult(
            Request(f"tv/{self.id}/similar"), locale=self._locale
        )
        res._name = f"Similar to {self.name}"
        return res
