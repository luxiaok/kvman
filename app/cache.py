#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

import redis

# Wrapper Redis
class RCache():

    def __init__(self,host,port=6379,db=0,password=''):
        self._host = host
        self._port = port
        self._db = db
        self._password = password

    def Connect(self):
        return redis.Redis(self._host, self._port, self._db, self._password)
