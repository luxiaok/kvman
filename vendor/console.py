#!/usr/bin/python
# -*- coding:utf8 -*-
# Powered By XK Studio

import sys
import os
sys.path.append(os.getcwd()+"/config")

import redis
import simplejson
from settings import kvman_settings as config
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
        if not token:
            return None
        arg = token.split(':')
        uuid = arg[0]
        real_token = arg[1]
        client = redis.Redis(self._server, self._port, self._db, self._password)
        stuff = client.get(self._key_pre + uuid)
        if stuff is None:
            return None
        else:
            data = simplejson.loads(stuff.decode("utf-8"))
            if data['token'] == real_token:
                return [data['host'], data['port']]
        return None


if __name__ == "__main__":
    websockify_init()
