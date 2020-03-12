#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from tornado.web import UIModule


# Hello
class Hello(UIModule):

    def render(self,foo):
        return self.render_string("ui_modules/hello.html", foo=foo)

# Test
class Test(UIModule):

    def render(self,foo):
        return foo
