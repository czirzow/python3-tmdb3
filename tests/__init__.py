# ----------------------------------------------
# Name: Abstract TestCase for `python3-tmdb3`
# Author: Pol Canelles <canellestudi@gmail.com>
# Year: 2019
# License: Creative Commons GNU GPL v2
# (http://creativecommons.org/licenses/GPL/2.0/)
# ----------------------------------------------

import os
from os.path import join
from unittest import TestCase
from abc import ABC, abstractmethod
from httpretty import HTTPretty

from tmdb3 import set_key, set_cache

# Here we set a fake api key because we perform our tests
# simulating internet calls with `httpretty` module, but if we need to update
# the tests data, then we should put in here a real api key.
FAKE_API_KEY = '00000000000000000000000000000000'

LOCALDIR = os.path.dirname(__file__)


# Method used to get get the expected
# json result to perform our tests
def get_json_result(filename):
    with open(filename) as fp:
        body = fp.read()
    return body


class AbstractTestTmdbCase(ABC, TestCase):
    """Abstract test data class. Defines an interface for subclasses
    that contain test data."""
    base_url = 'http://api.themoviedb.org/3/'
    api_key = FAKE_API_KEY
    cache_file = None

    @property
    @abstractmethod
    def mock_data(self):
        """Subclasses must have property 'mock_data'. It should be a dictionary
        containing tuples: the url to mock and the json file with the
        appropriate response."""
        return NotImplemented

    @property
    @abstractmethod
    def mock_requests(self):
        """Subclasses must have property 'mock_requests'. It should be a tuple,
        containing the url to mock and the json file with the appropriate
        response."""
        return NotImplemented

    def setUp(self):
        set_key(FAKE_API_KEY)
        if self.cache_file:
            set_cache(filename=self.cache_file)
        else:
            set_cache(engine='null')

        for mock_key in self.mock_requests:
            mock_json_file, mock_url = self.mock_data[mock_key]
            body = get_json_result(join(LOCALDIR, 'data', mock_json_file))
            HTTPretty.register_uri(
                HTTPretty.GET,
                mock_url.format(base_url=self.base_url, api=self.api_key),
                body=body
            )
