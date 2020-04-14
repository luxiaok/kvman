#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

config = {
    'db': {
        'host': 'db.xk.com',
        'port': 3306,
        'db': 'kvman',
        'user': 'test',
        'passwd': 'test',
        'charset': 'utf8'
    },
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'password': '',
        'db': '0'
    },
    'app_settings': dict(
        template_path = 'view',
        static_path = 'static',
        static_url_prefix = '/static/',
        xsrf_cookies = False,
        cookie_secret = "db884468559f4c432bf1c1775f3dc9da",
        cookie_name = 'kvman',
        session_prefix = "kvman_session_",
        session_expires = 7200,
        login_url = "/user/login",
        users_key = "kvman_users",
        default_lang = "en_US",
        debug = True,
        autoreload = True
    )
}
