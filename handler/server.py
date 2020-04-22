#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Server Page

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth
from service.kvm import kvm
import json


class IndexHandler(BaseHandler):

    @Auth
    def get(self):
        servers = self.get_kvm_server()
        for i in servers:
            k = kvm(config=i)
            i['guests'] = k.getGuestsNum()
        self.render('server/index.html',data=servers)


class CreateHandler(BaseHandler):

    @Auth
    def post(self):
        hostname = self.get_argument('hostname')
        port = self.get_argument('port')
        protocol = self.get_argument('protocol')
        username = self.get_argument('username')
        password = self.get_argument('password')
        comments = self.get_argument('comments')
        if not hostname or not protocol:
            return self.returnJson({'code': -1, 'msg': u'请填写主机名和协议！'})
        host = self.get_kvm_server(hostname)
        if host:
            return self.returnJson({'code': -1, 'msg': u'主机名重复！'})
        data = {
            'hostname': hostname,
            'port': port or None,
            'protocol': protocol,
            'username': username or '',
            'password': password or '',
            'default': False,
            'comments': comments or ''
        }
        result = self.redis.hset(self.application.settings['kvm_servers_key'], hostname, json.dumps(data))
        if result:
            return self.returnJson({'code': 0, 'msg': u'成功添加了一台 KVM 服务器！'})
        else:
            return self.returnJson({'code': -1, 'msg': u'添加失败！'})
