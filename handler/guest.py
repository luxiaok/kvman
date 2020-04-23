#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Guests

from BaseHandler import BaseHandler
from service.kvm import kvm
from tornado.web import authenticated as Auth
from vendor import functions as fun
import json


guest_status = {
    kvm.VIR_DOMAIN_NOSTATE: u'<span style="color:#ccc;">未知</span>',
    kvm.VIR_DOMAIN_RUNNING: u'<span style="color:green;">运行中</span>',
    kvm.VIR_DOMAIN_BLOCKED: u'<span style="color:#ccc;">Blocked</span>',
    kvm.VIR_DOMAIN_PAUSED: u'<span style="color:#ccc;">已挂起</span>',
    kvm.VIR_DOMAIN_SHUTDOWN: u'<span style="color:#ccc;">已关机</span>',
    kvm.VIR_DOMAIN_SHUTOFF: u'<span style="color:#ccc;">已关机</span>',
    kvm.VIR_DOMAIN_CRASHED: u'<span style="color:red;">Crashed</span>',
    kvm.VIR_DOMAIN_PMSUSPENDED: u'<span style="color:red;">PMSUSPENDED</span>'
}


class IndexHandler(BaseHandler):

    @Auth
    def get(self):
        guests = self.kvm.getGuests()
        status = [u'<span style="color:#ccc;">已关机</span>',u'<span style="color:green;">运行中</span>']
        self.render('guest/index.html',guests=guests,status=status,state=guest_status)


class AutostartHandler(BaseHandler):

    @Auth
    def post(self):
        name = self.get_argument('name')
        flag = self.get_argument('flag') # 0 or 1
        self.kvm.setAutostart(name,int(flag))
        self.returnJson({'code': 0, 'msg': u'操作成功！'})


class StartHandler(BaseHandler):

    @Auth
    def post(self):
        name = self.get_argument('name')
        result = self.kvm.startGuest(name)
        if result:
            code = 0
            msg = u'已开机！'
        else:
            code = -1
            msg = u'开机失败：%s' % self.kvm._msg
        self.returnJson({'code': code, 'msg': msg})


class ShutdownHandler(BaseHandler):

    @Auth
    def post(self):
        name = self.get_argument('name')
        force = self.get_argument('force','no')
        force = False if force=='no' else True
        result = self.kvm.shutdownGuest(name,force)
        if result:
            code = 0
            msg = u'正在关机……'
        else:
            code = -1
            msg = u'关机失败：%s' % self.kvm._msg
        self.returnJson({'code': code, 'msg': msg})


class RebootHandler(BaseHandler):

    @Auth
    def post(self):
        name = self.get_argument('name')
        result = self.kvm.rebootGuest(name)
        self.returnJson({'code':0,'result':result,'msg':self.kvm._msg})


class CreateGuestHandler(BaseHandler):

    @Auth
    def get(self):
        self.render('guest/create.html')


class DetailHandler(BaseHandler):

    @Auth
    def get(self):
        name = self.get_argument('name')
        sid = self.get_argument('sid', None)
        k = self.kvm(sid)
        guest = k.getGuest(name)
        self.render('guest/detail.html',name=name)


# 远程连接
class ConsoleHandler(BaseHandler):

    @Auth
    def get(self):
        token = self.get_argument('token')
        key = "%s%s" % (self.application.settings['kvman_console_token_key_pre'],token)
        stuff = self.redis.get(key)
        guest = ''
        if stuff:
            data = json.loads(stuff)
            guest = data['guest']
        self.render('guest/console.html',guest=guest,token=token)


    # 生成远程访问的Token
    @Auth
    def post(self):
        guest = self.get_argument('guest',None)
        if not guest:
            return self.returnJson({'code': -1, 'msg': u'该主机不存在！'})
        sid = self.get_argument('sid', None)
        k = self.kvm(sid)
        address = k.getVncAddress(guest)
        if not address['port'] or address['port'] == -1:
            return self.returnJson({'code': -1, 'msg': u'该主机未开机！'})
        data = {
            'guest': guest,
            'host': address['host'], # VNC Server Adress
            'port': address['port']  # VNC Port
        }
        token = fun.random_str(64)
        key_pre = self.application.settings['kvman_console_token_key_pre']
        key_expire = self.application.settings['kvman_console_token_expire']
        self.redis.setex(key_pre+token,key_expire,json.dumps(data))
        ret = {
            'guest': guest,
            'token': token,
            'port': 6080 # WebSocket Port
        }
        self.returnJson({'code': 0, 'data': ret, 'msg': 'success'})


# 退出远程连接
class ConsoleExitHandler(BaseHandler):

    @Auth
    def post(self):
        token = self.get_argument('token')
        key = "%s%s" % (self.application.settings['kvman_console_token_key_pre'], token)
        self.redis.delete(key)
        return self.returnJson({'code': 0, 'msg': 'success'})
