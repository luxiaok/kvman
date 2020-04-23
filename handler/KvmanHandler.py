#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# 2020-04-22

import json
from service.kvm import kvm

class KvmanHandler:

    # 获取 Kvm Server 配置
    def get_kvm_server(self, hostname=None):
        key = self.application.settings['kvm_servers_key']
        if hostname:
            stuff = self.redis.hget(key, hostname)
            if stuff:
                servers = json.loads(stuff)
            else:
                servers = None
        else:
            stuff = self.redis.hgetall(key)
            if stuff:
                servers = [json.loads(stuff[i]) for i in stuff]
                servers = sorted(servers,key=lambda item : item['hostname']) # Sort by hostname
            else:
                servers = []
        return servers


    def kvm(self,sid=None,set_sid=True):
        if sid:
            server = self.get_kvm_server(sid)  # uri, string
            if server:
                if set_sid:
                    self.set_kvm_sid(sid)
                return kvm(server)
        else:
            sid = self.get_kvm_sid() # 是否有缓存SID
            if sid:
                server = self.get_kvm_server(sid)  # uri, string
                if server:
                    return kvm(server)
            else: # 没有sid参数，检测是否只有一个Kvm Server
                server_count = self.redis.hlen(self.application.settings['kvm_servers_key'])
                if server_count == 1:
                    server = self.get_kvm_server()
                    if set_sid:
                        self.set_kvm_sid(server[0]['hostname']) # 缓存sid
                    return kvm(server[0])  # dict
        return None


    def set_kvm_sid(self,sid):
        if sid:
            self.session.data['kvm_sid'] = sid


    def get_kvm_sid(self):
        return self.session.data.get('kvm_sid',None)
