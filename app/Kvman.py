#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.netutil
import tornado.process
import tornado.locale
import tornado.options
import platform
import logging
#import db
from cache import RCache
from tornado.log import gen_log, LogFormatter
from handler.page import Page404Handler
from config.settings import *
from handler import route
from ui_modules import UIModules
from Template import TemplateLoader # For Jinja2
from tornado.options import define, options

define("host", default='0.0.0.0', help="Listen on the given IP", type=str)
define("port", default=8081, help="Run on the given port", type=int)

# Call options.*** should be after the parse_command_line()
tornado.options.parse_command_line()

class App(tornado.web.Application):

    def __init__(self,handlers,conf,log):
        self.__version__ = conf['version']
        self.log = log
        settings = conf['app_settings']
        settings['default_handler_class'] = Page404Handler  # 404

        # Don't Support for Jinja2
        #settings['ui_modules'] = UIModules
        #tornado.web.Application.__init__(self, handlers, **settings)
        #super(App, self).__init__(handlers, **settings)

        # Support for Jinja2
        tpl_loader = TemplateLoader(settings['template_path'], False)
        tornado.web.Application.__init__(self, handlers, template_loader=tpl_loader.Loader(), **settings)
        super(App, self).__init__(handlers, template_loader=tpl_loader.Loader(), **settings)

        #每10秒执行一次
        #tornado.ioloop.PeriodicCallback(self.test, 1 * 10 * 1000).start()

        # Init Database
        #self.db = db.DB(**conf['db'])

        #Init Redis
        R = RCache(**conf['redis'])
        self.redis = R.Connect()

        # Load Locale
        self.__load_locale(settings['default_lang'])


    #def test(self):
    #    self.log.info('Test')

    # Load Locale
    def __load_locale(self,default_lang):
        tornado.locale.load_translations('locale')
        tornado.locale.set_default_locale(default_lang)

class Kvman():

    def __init__(self,processes=4):
        self.__version__ = '1.0.0'
        self.host = options.host
        self.port = options.port
        self.urls = route
        self.config = config
        self.config['version'] = self.__version__
        self.init_log()
        self.log = gen_log
        if platform.system() == "Linux":  #根据操作系统类型来确定是否启用多线程
            self.processes = processes # 当processes>1时，PeriodicCallback定时任务会响相应的执行多次
        else:
            self.processes = 1
        self.log.info('Tornado Web Server: %s' % tornado.version)
        self.log.info('Kvman %s' % self.__version__)  # 启动时打印版本号
        self.log.info('Listen Port: %s' % self.port)

    def init_log(self):
        datefmt = '%Y-%m-%d %H:%M:%S'
        fmt = '%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'
        formatter = LogFormatter(color=True, datefmt=datefmt, fmt=fmt)
        root_log = logging.getLogger()
        for logHandler in root_log.handlers:
            logHandler.setFormatter(formatter)

    # Single Process
    def single_process(self):
        http_app = App(self.urls, self.config, self.log)

        # Single Process 1
        # http_app.listen(self.port)
        # tornado.ioloop.IOLoop.current().start()

        # Single Process 2
        http_server = tornado.httpserver.HTTPServer(request_callback=http_app, xheaders=True)
        http_server.listen(self.port)
        tornado.ioloop.IOLoop.current().start()

    # Multi Process
    def multi_process(self):
        http_app = App(self.urls, self.config, self.log)
        http_sockets = tornado.netutil.bind_sockets(self.port, self.host)
        tornado.process.fork_processes(num_processes=self.processes)
        http_server = tornado.httpserver.HTTPServer(request_callback=http_app, xheaders=True)
        http_server.add_sockets(http_sockets)
        tornado.ioloop.IOLoop.current().start()

    def run(self, multi=False):
        if multi:
            self.multi_process()
        else:
            self.single_process()
