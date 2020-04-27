#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Index Page

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth


class IndexHandler(BaseHandler):

    @Auth
    def get(self):
        self.render('event/index.html')
