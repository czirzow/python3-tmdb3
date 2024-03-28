#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------
# Name: cache_redis.py
# Python Library
# Author: Curt Zirzow
# Purpose: Cache with a redis. 
# -----------------------

from .cache_engine import CacheEngine, CacheObject
import json
import redis

DEBUG = False
if DEBUG:
    import logging


class RedisCacheObject(CacheObject):

    def __init__(self, *args, **kwargs):
        self._key = None
        self._data = None
        self._size = None
        self._buff = None
        super(RedisCacheObject, self).__init__(*args, **kwargs)
    
    @property
    def key(self):
        return None

    @key.setter
    def key(self, value):
        self._key = value
        
    
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self,value):
        self._data = value
    



class RedisEngine(CacheEngine):
    """Cache items to a redis configuration"""

    name = "redis"
    server = None

    def __init__(self, parent):
        self.configure(None)

    def configure(self, *args, **kwargs):
        self.server = redis.Redis(*args, **kwargs)
        pass

    @property
    def is_remote(self):
        return True

    def get(self, key):
        data = self.server.get(key)
        if DEBUG:
            logging.warning(f".get(key): {key}")
        if data is None:
            return None
        return RedisCacheObject(key, json.loads(data))

    def put(self, key, value, lifetime):
        rc = self.server.set(key, json.dumps(value))
        if DEBUG:
            logging.warning(f"set({key} rc[{rc}]")
        return RedisCacheObject(key, value, lifetime)

    def expire(self, key):
        pass





