#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By Luxiaok

import libvirt
from xml.dom import minidom
from config.settings import config


class kvm:

    def __init__(self):
        uri = 'qemu:///system'
        self.conn = self.openConnect(uri)


    def openConnect(self,uri):
        return libvirt.openReadOnly(uri)


    def close(self):
        self.conn.close()


    # disks = xml.getElementsByTagName('disk')
    def getHdd(self,disks):
        hdd = []
        type_to_path = {'file': 'file', 'block': 'dev'}
        if len(disks) > 0:
            for d in disks:
                if d.getAttribute('device') == 'disk':  # disk or cdrom
                    hdd_type = d.getAttribute('type') # file or block
                    hddNodes = d.childNodes
                    for n in hddNodes:
                        if n.nodeName == 'source':
                            hdd_path = n.getAttribute(type_to_path[hdd_type]) # hdd src, eg: /kvm/images/guest.img
                            vol = self.conn.storageVolLookupByPath(hdd_path)
                            info = vol.info()
                            total = info[1]/1024.0/1024/1024
                            used = info[2]/1024.0/1024/1024
                            hdd.append("%.2f G / %.2f G" % (used,total))
        return hdd


    def getGuests(self):
        guests = []
        doms = self.conn.listAllDomains(0)
        for i in doms:
            raw_xml = i.XMLDesc(0)
            xml = minidom.parseString(raw_xml)
            tag_title = xml.getElementsByTagName('title')
            title = tag_title[0].childNodes[0].nodeValue
            tag_desc = xml.getElementsByTagName('description')
            desc = tag_desc[0].childNodes[0].nodeValue
            state,maxmem,mem,cpus,cpu_time = i.info()
            hdd = self.getHdd(xml.getElementsByTagName('disk'))
            dom = {
                'id': i.ID(),
                'name': i.name(),
                'title': title,
                'desc': desc,
                'os_type': i.OSType(),
                'cpu': cpus,
                'mem': str(mem/1024/1024) + ' GB' ,
                'hdd': hdd,
                'network': '',
                'status': i.isActive()
            }
            guests.append(dom)
        return guests

