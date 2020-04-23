#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth


class IndexHandler(BaseHandler):

    @Auth
    def get(self):
        sid = self.get_argument('sid', None)
        k = self.kvm(sid)
        if k:
            storages = k.getStoragePools()
        else:
            storages = []
        self.render('storage/index.html',sid=sid,storages=storages)


class VolumeHandler(BaseHandler):

    @Auth
    def get(self):
        pool = self.get_argument('pool')
        sid = self.get_argument('sid', None)
        k = self.kvm(sid)
        if k:
            vols = k.getStorageVols(pool)
        else:
            vols = []
        self.render('storage/volume.html',sid=sid,vols=vols,pool=pool)
