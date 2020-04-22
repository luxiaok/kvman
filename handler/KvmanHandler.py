#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# 2020-04-22

import json

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
            else:
                servers = []
        return servers
