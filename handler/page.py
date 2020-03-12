#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler

# 404 Page
class Page404Handler(BaseHandler):
    def get(self):
        self.render('page/404.html', title="404")

# 500 Page
class Page500Handler(BaseHandler):
    def get(self):
        self.render('page/500.html', title="500")

# Error Page
class PageErrorHandler(BaseHandler):
    def get(self):
        self.render('page/error.html', title="Error")

# Blank Page
class BlankHandler(BaseHandler):
    def get(self):
        self.render('page/blank.html', title="Blank")