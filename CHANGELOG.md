# Changelog

## [0.8.1] - 2019/05/07
-  Add discover methods:
     * discoverTv
     * discoverMovie
## [0.8.0] - 2019/03/17
- CI integration with coverage
- Add tests
- Add `CHANGELOG.md` file
- Add Python 3.6+ support
- Drop Python2 support
## [0.7.2] - 2015/01/18
- Add similar and keywords to TV Series
- Fix unicode issues with search result object names
- Temporary fix for youtube videos with malformed URLs
## [0.7.1] - 2015/01/18
- Add rate limiter to cache engine
## [0.7.0] - 2013/11/29
- Add support for `television` series data
## [0.6.17] - 2013/06/29
- Add `userrating`/`votes` to Image
- Add overview to Collection
- Remove `releasedate` sorting from Collection Movies
## [0.6.16] - 2012/12/04
- Make absent primary images return None (previously u'')
## [0.6.15] - 2012/12/03
- Add ability to search Collections
## [0.6.14] - 2012/12/03
- Add support for Lists
## [0.6.13] - 2012/08/19
- Fix URL for rating Movies
## [0.6.12] - 2012/08/19
- Add support for Movie watchlist query and editing
## [0.6.11] - 2012/08/19
- Fix URL for top rated Movie query
## [0.6.10] - 2012/08/19
- Add upcoming movie classmethod
## [0.6.9] - 2012/08/19
- Correct Movie image language filtering
## [0.6.8] - 2012/08/19
- Add support for collection images
## [0.6.7] - 2012/07/07
- Add support for searching by year
## [0.6.6] - 2012/07/02
- Turn date processing errors into mutable warnings
## [0.6.5] - 2012/07/02
- Prevent data from being blanked out by subsequent queries
## [0.6.4] - 2012/06/21
- Add Genre list and associated Movie search
## [0.6.3] - 2012/06/21
- Add Studio search
## [0.6.2] - 2012/05/03
- Add similar movie search for Movie objects
## [0.6.1] - 2012/04/30
- Add adult filtering for people searches
## [0.6.0] - 2012/04/15
- Add user authentication support
## [0.5.0] - 2012/04/11
- Rework cache framework and improve file cache performance
## [0.4.6] - 2012/04/01
- Add slice support for search results
## [0.4.5] - 2012/04/01
- Add locale fallthrough for images and alternate titles
## [0.4.4] - 2012/03/30
- Add support for additional Studio information
## [0.4.3] - 2012/03/30
- Add a few missed Person properties
## [0.4.2] - 2012/03/27
- Improve cache file selection for Windows systems
## [0.4.1] - 2012/03/26
- Add custom classmethod for dealing with IMDB movie IDs
## [0.4.0] - 2012/03/26
- Add full locale support (language and country) and optional fall through
## [0.3.7] - 2012/03/25
- Generalize caching mechanism, and allow controllability
## [0.3.6] - 2012/03/22
- Rework paging mechanism
## [0.3.5] - 2012/03/22
- Add methods for grabbing current, popular, and top rated movies
## [0.3.4] - 2012/03/03
- Re-enable search paging
## [0.3.3] - 2012/03/03
- Add functional language support
## [0.3.2] - 2012/03/03
- Remove MythTV key from results.py
## [0.3.1] - 2012/02/19
- Add collection support
## [0.3.0] - 2012/01/18
- Rework backend machinery for managing OO interface to results
## [0.2.1] - 2012/01/07
- Temporary work around for broken search paging
## [0.2.0] - 2012/01/07
- Add caching mechanism for API queries
## [0.1.0] - 2012/01/06
- Initial development
