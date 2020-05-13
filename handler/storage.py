#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth
import libvirt


class IndexHandler(BaseHandler):

    @Auth
    def get(self):
        print storage_type
        storages = self.kvm.getStoragePools()
        self.render('storage/index.html',storages=storages)


class VolumeHandler(BaseHandler):

    @Auth
    def get(self):
        pool = self.get_argument('pool')
        vols = self.kvm.getStorageVols(pool)
        self.render('storage/volume.html',vols=vols,pool=pool)

