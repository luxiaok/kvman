#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Index Page

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth

class IndexHandler(BaseHandler):

    @Auth
    def get(self):
        version = self.kvm.getVersion()
        version['app'] = self.app_version
        self.render('index/index.html',version=version)
