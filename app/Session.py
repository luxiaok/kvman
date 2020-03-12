#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Session Support For Tornado

import hashlib
import os
import time
import json


class Session:


    def __init__(self,prefix='',session_id=None,expires=7200,redis=None):
        self.redis = redis
        self.expires = expires
        self.prefix = prefix
        if session_id:
            self.session_id = prefix + session_id
            self.data = self.get_data()
            if self.data:
                self.isGuest = False
            else:
                self.isGuest = True # Not Login
        else:
            self.session_id = None
            self.data = {} # Null Dict
            self.isGuest = True # Not Login


    # 生成SessionID
    def gen_session_id(self):
        sid = hashlib.sha1('%s%s' % (os.urandom(16), time.time())).hexdigest()
        self.session_id = self.prefix + sid
        return sid


    # 获取Session数据
    def get_data(self):
        session = self.redis.get(self.session_id)
        if not session:
            return None
        session = json.loads(session) # 字符串转字典
        return session


    # Get
    def get(self,name):
        if name and self.data:
            return self.data.get(name,None)
        else:
            return None


    # Set
    def set(self,name,value):
        self.data[name] = value


    def save(self):
        if not self.isGuest and self.session_id and self.data:
            self.redis.set(self.session_id,json.dumps(self.data),self.expires)


    # 销毁Session
    def remove(self):
        if self.session_id: # SessionID存在
            self.redis.delete(self.session_id)
            self.session_id = None
            self.data = None
            self.isGuest = True
