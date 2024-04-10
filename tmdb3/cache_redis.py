#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------
# Name: cache_redis.py
# Python Library
# Author: Curt Zirzow
# Purpose: Cache with a redis. 
# -----------------------

from .tmdb_exceptions import *
from .cache_engine import CacheEngine, CacheObject
import json

# FIXME: allow this to fail safely 
# or move to init and do a graceful catch
# in the case the person doesn't even intend to use redis
# 
import redis
#/

DEBUG = False

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
        try:
            self.server = redis.Redis(*args, **kwargs)
            self.server.ping()
        except Exception as error:
            raise TMDBRedisError(error)


    @property
    def is_remote(self):
        return True

    def get(self, key):
        data = self.server.get(key)
        if DEBUG:
            print(f"get(key): {key}")
        if data is None:
            return None
        return RedisCacheObject(key, json.loads(data))

    def put(self, key, value, lifetime):
        #TODO: add lifetime
        rc = self.server.set(key, json.dumps(value))
        if DEBUG:
            print(f"set({key} rc[{rc}]")
        return RedisCacheObject(key, value, lifetime)

    def expire(self, key):
        """ redis will handle the expiration of keys"""
        pass





