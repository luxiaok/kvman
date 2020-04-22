#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler

# 404 Page
class Page404Handler(BaseHandler):
    def get(self):
        self.render('page/404.html')

# 500 Page
class Page500Handler(BaseHandler):
    def get(self):
        self.render('page/500.html')

# Error Page
class PageErrorHandler(BaseHandler):
    def get(self):
        self.render('page/error.html',msg='Error')
