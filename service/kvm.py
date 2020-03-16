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
        self._code = 0
        self._msg = 'success'


    def openConnect(self,uri):
        #return libvirt.openReadOnly(uri)
        return libvirt.open(uri)


    def close(self):
        self.conn.close()


    def getGuest(self,name):
        try:
            dom = self.conn.lookupByName(name)
        except:
            dom = None
            self._code = -1
            self._msg = 'Not found guest: ' + name
        return dom


    # disks = xml.getElementsByTagName('disk')
    def getHdd(self,disks):
        hdd = []
        type_to_path = {'file': 'file', 'block': 'dev'}
        for d in disks:
            if d.getAttribute('device') == 'disk': # disk or cdrom
                hdd_type = d.getAttribute('type')  # file or block
                hddNodes = d.childNodes
                for n in hddNodes:
                    if n.nodeName == 'source':
                        hdd_path = n.getAttribute(type_to_path[hdd_type])  # hdd src, eg: /kvm/images/guest.img
                        vol = self.conn.storageVolLookupByPath(hdd_path)
                        info = vol.info()
                        total = info[1] / 1024.0 / 1024 / 1024
                        used = info[2] / 1024.0 / 1024 / 1024
                        hdd.append("%.2f G / %.2f G" % (used, total))
        return hdd


    def getNetwork(self,interfaces):
        net = []
        for i in interfaces:
            type = i.getAttribute('type')
            iNodes = i.childNodes
            mac,link,drive = ('','','')
            for tag in iNodes:
                if tag.nodeName == 'mac':
                    mac = tag.getAttribute('address')
                elif tag.nodeName == 'source':
                    link = tag.getAttribute(type) # kvm network pool name,eg: default,br0,...
                elif tag.nodeName == 'model':
                    drive = tag.getAttribute('type') # e1000,virtio,...
                else:
                    pass
            net.append('%s -> %s' % (mac,link))
        return net


    def getGuests(self):
        guests = []
        doms = self.conn.listAllDomains(0)
        for i in doms:
            raw_xml = i.XMLDesc(0)
            xml = minidom.parseString(raw_xml)
            tag_title = xml.getElementsByTagName('title')
            title = tag_title[0].childNodes[0].nodeValue if len(tag_title) > 0 else ''
            tag_desc = xml.getElementsByTagName('description')
            desc = tag_desc[0].childNodes[0].nodeValue if len(tag_desc) > 0 else ''
            state,maxmem,mem,cpus,cpu_time = i.info()
            hdd = self.getHdd(xml.getElementsByTagName('disk'))
            network = self.getNetwork(xml.getElementsByTagName('interface'))
            state,reason = i.state()
            dom = {
                'id': i.ID(),
                'name': i.name(),
                'title': title,
                'desc': desc,
                'os_type': i.OSType(), # hvm, useless
                'cpu': cpus,
                'mem': str(mem/1024/1024) + ' GB' ,
                'hdd': hdd,
                'network': network,
                'state': state,
                'status': i.isActive()
            }
            guests.append(dom)
        return guests


    def startGuest(self,name):
        dom = self.conn.lookupByName(name)
        if not dom:
            return False
        if dom.create() < 0:
            return False
        else:
            return True


    def shutdownGuest(self,name,force=False):
        dom = self.conn.lookupByName(name)
        if not dom:
            return False
        if force:
            result = dom.destroy()
        else:
            result = dom.shutdown()
        return result


