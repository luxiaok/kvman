#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth
from service.kvm import kvm

class IndexHandler(BaseHandler):

    @Auth
    def get(self):
        #self.log.info('Hello,Index page!') # Log Test
        k = kvm()
        storages = k.getStoragePools()
        self.render('storage/index.html',storages=storages)


class VolumeHandler(BaseHandler):

    @Auth
    def get(self):
        pool = self.get_argument('pool')
        k = kvm()
        vols = k.getStorageVols(pool)
        self.render('storage/volume.html',vols=vols,pool=pool)
