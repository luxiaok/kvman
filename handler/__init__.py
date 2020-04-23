#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

import index
import server
import guest
import storage
import network
import monitor
import setting
import page
import user

route = [
    (r'/',index.IndexHandler),
    (r'/server',server.IndexHandler),
    (r'/server/create',server.CreateHandler),
    (r'/server/update',server.UpdateHandler),
    (r'/server/delete',server.DeleteHandler),
    (r'/guest',guest.IndexHandler),
    (r'/guest/create',guest.CreateGuestHandler),
    (r'/guest/detail',guest.DetailHandler),
    (r'/guest/autostart',guest.AutostartHandler),
    (r'/guest/start',guest.StartHandler),
    (r'/guest/shutdown',guest.ShutdownHandler),
    (r'/guest/reboot',guest.RebootHandler),
    (r'/guest/console',guest.ConsoleHandler),
    (r'/guest/console-exit',guest.ConsoleExitHandler),
    (r'/storage',storage.IndexHandler),
    (r'/storage/volume',storage.VolumeHandler),
    (r'/network',network.IndexHandler),
    (r'/monitor',monitor.IndexHandler),
    (r'/setting',setting.IndexHandler),
    (r'/setting/install',setting.InstallHandler),
    (r'/user/login',user.LoginHandler),
    (r'/user/logout',user.LogoutHandler),
    (r'/user/passwd',user.PasswdHandler),
    (r'/user/profile',user.ProfileHandler),
    #(r'/user/register',user.RegisterHandler),
    (r'/page/404.html',page.Page404Handler),
    (r'/page/500.html',page.Page500Handler),
    (r'/page/error.html',page.PageErrorHandler)
]
