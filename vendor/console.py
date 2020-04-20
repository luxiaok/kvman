#!/usr/bin/python
# -*- coding:utf8 -*-
# Powered By XK Studio

import sys
import os
sys.path.append(os.getcwd()+"/config")

import redis
import simplejson
from settings import config
from websockify.websocketproxy import websockify_init

class Token:

    def __init__(self, src):
        # token-source == src
        self._server = config['redis']['host']
        self._port = config['redis']['port']
        self._db = config['redis']['db']
        self._password = config['redis']['password']
        self._key_pre = config['app_settings']['kvman_console_token_key_pre']


    def lookup(self, token):

        client = redis.Redis(self._server,self._port,self._db,self._password)
        key = self._key_pre + token
        stuff = client.get(key)
        if stuff is None:
            return None
        else:
            data = simplejson.loads(stuff.decode("utf-8"))
            return [ data['host'], data['port'] ]


if __name__ == "__main__":
    websockify_init()
