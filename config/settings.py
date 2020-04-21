#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

config = {
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
        kvm_servers_key = "kvman_kvm_servers",
        kvman_console_token_key_pre = "kvman_console_token_",
        kvman_console_token_expire = 3600,
        default_lang = "en_US",
        debug = True,
        autoreload = True
    )
}
