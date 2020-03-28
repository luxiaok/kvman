#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio


from BaseHandler import BaseHandler
#from tornado.web import authenticated as Auth
from service.kvm import kvm

class IndexHandler(BaseHandler):

    #@Auth
    def get(self):
        #self.log.info('Hello,Index page!') # Log Test
        k = kvm()
        storages = k.getStoragePools()
        self.title = u'存储'
        self.render('storage/index.html',storages=storages)


class VolumeHandler(BaseHandler):

    #@Auth
    def get(self):
        #k = kvm()
        self.title = u'存储卷'
        self.render('storage/volume.html')
