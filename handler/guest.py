#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Guests

from BaseHandler import BaseHandler
from service.kvm import kvm
#from tornado.web import authenticated as Auth
import libvirt

guest_status = {
    libvirt.VIR_DOMAIN_NOSTATE: u'<span style="color:#ccc;">未知</span>',
    libvirt.VIR_DOMAIN_RUNNING: u'<span style="color:green;">运行中</span>',
    libvirt.VIR_DOMAIN_BLOCKED: u'<span style="color:#ccc;">Blocked</span>',
    libvirt.VIR_DOMAIN_PAUSED: u'<span style="color:#ccc;">已挂起</span>',
    libvirt.VIR_DOMAIN_SHUTDOWN: u'<span style="color:#ccc;">已关机</span>',
    libvirt.VIR_DOMAIN_SHUTOFF: u'<span style="color:#ccc;">已关机</span>',
    libvirt.VIR_DOMAIN_CRASHED: u'<span style="color:red;">Crashed</span>',
    libvirt.VIR_DOMAIN_PMSUSPENDED: u'<span style="color:red;">PMSUSPENDED</span>'
}

class IndexHandler(BaseHandler):

    #@Auth
    def get(self):
        k = kvm()
        guests = k.getGuests()
        k.close()
        status = [u'<span style="color:#ccc;">已关机</span>',u'<span style="color:green;">运行中</span>']
        self.title = u'虚拟机实例'
        self.render('guest/index.html',guests=guests,status=status,state=guest_status)


class StartHandler(BaseHandler):

    def post(self):
        name = self.get_argument('name')
        k = kvm()
        result = k.startGuest(name)
        self.jsonReturn({'code':0,'result':result,'msg':k._msg})


class ShutdownHandler(BaseHandler):

    def post(self):
        name = self.get_argument('name')
        force = self.get_argument('force','no')
        force = False if force=='no' else True
        k = kvm()
        result = k.shutdownGuest(name,force)
        self.jsonReturn({'code':0,'result':result,'msg':k._msg})


class CreateGuestHandler(BaseHandler):

    def get(self):
        self.title = u'创建虚拟机'
        self.render('guest/create.html')


class DetailHandler(BaseHandler):

    def get(self):
        name = self.get_argument('name')
        self.title = u'虚拟机详情 - ' + name
        self.render('guest/detail.html',name=name)

