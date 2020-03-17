#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Index Page

from BaseHandler import BaseHandler
#from tornado.web import authenticated as Auth
from service.kvm import kvm

class IndexHandler(BaseHandler):

    #@Auth
    def get(self):
        #self.log.info('Hello,Index page!') # Log Test
        k = kvm()
        version = k.getVersion()
        version['app'] = self.app_version
        self.title = u'控制台'
        self.render('index/index.html',version=version)
