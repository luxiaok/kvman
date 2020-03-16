#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

import index
import guest
import storage
import network
import monitor
import page
import user

route = [
    (r'/',index.IndexHandler),
    (r'/guest',guest.IndexHandler),
    (r'/guest/create',guest.CreateGuestHandler),
    (r'/guest/detail',guest.DetailHandler),
    (r'/guest/start',guest.StartHandler),
    (r'/guest/shutdown',guest.ShutdownHandler),
    (r'/storage',storage.IndexHandler),
    (r'/network',network.IndexHandler),
    (r'/monitor',monitor.IndexHandler),
    (r'/user/login',user.LoginHandler),
    (r'/user/register',user.RegisterHandler),
    (r'/page/404.html',page.Page404Handler),
    (r'/page/500.html',page.Page500Handler),
    (r'/page/error.html',page.PageErrorHandler),
    (r'/page/blank.html',page.BlankHandler),
]
