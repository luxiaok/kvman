#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By Luxiaok

import libvirt
from xml.dom import minidom
from config.settings import kvm as kconfig


class kvm:

    def __init__(self):
        self.conn = self.openConnect()


    def openConnect(self):
        return libvirt.openReadOnly(None)


    def close(self):
        self.conn.close()


    def getGuests(self):
        guests = []
        doms = self.conn.listAllDomains()
        for i in doms:
            raw_xml = i.XMLDesc(0)
            xml = minidom.parseString(raw_xml)
            tag_title = xml.getElementsByTagName('title')
            title = tag_title[0].childNodes[0].nodeValue
            tag_desc = xml.getElementsByTagName('description')
            desc = tag_desc[0].childNodes[0].nodeValue
            dom = {
                'id': i.ID(),
                'name': i.name(),
                'title': title,
                'desc': desc,
                'cpu': '',
                'mem': '',
                'disk': '',
                'network': '',
                'status': i.isActive()
            }
            guests.append(dom)
        return guests

