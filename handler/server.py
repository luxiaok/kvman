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


# 编辑KVM主机信息
class UpdateHandler(BaseHandler):

    @Auth
    def post(self):
        hostname0 = self.get_argument('hostname0') # 原始主机名
        hostname = self.get_argument('hostname') # 新主机名
        port = self.get_argument('port')
        protocol = self.get_argument('protocol')
        username = self.get_argument('username')
        password = self.get_argument('password')
        comments = self.get_argument('comments')
        delete_host0 = False
        if not hostname or not protocol:
            return self.returnJson({'code': -1, 'msg': u'请填写主机名和协议！'})
        if hostname == hostname0: # 未改变主机名
            host = self.get_kvm_server(hostname0) # 读取主机信息
        else: # 修改了主机名
            host = self.get_kvm_server(hostname) # 检测新主机名是否重复
            if host:
                return self.returnJson({'code': -1, 'msg': u'主机名重复！'})
            delete_host0 = True
            host = {'hostname': hostname}
        host['port'] = port
        host['protocol'] = protocol
        host['username'] = username
        host['password'] = password
        host['comments'] = comments
        self.redis.hset(self.application.settings['kvm_servers_key'], hostname, json.dumps(host))
        if delete_host0:
            self.redis.hdel(self.application.settings['kvm_servers_key'], hostname0)
        return self.returnJson({'code': 0, 'msg': u'保存成功！'})


# 删除
class DeleteHandler(BaseHandler):

    @Auth
    def post(self):
        hostname = self.get_argument('hostname')
        host = self.get_kvm_server(hostname)
        if not host:
            return self.returnJson({'code': -1, 'msg': u'Kvm主机已被删除或不存在！'})
        self.redis.hdel(self.application.settings['kvm_servers_key'], hostname)
        return self.returnJson({'code': 0, 'msg': u'删除成功！'})
