/**
 * Kvm-Man
 * Powered By Luxiaok
 * https://github.com/luxiaok/kvman
 * */

import { k,route } from './kvman-lib.js?_v=20.4.25.1';

$(function () {

    var debug = true;

    var kvman = {
        foo: 'bar',
        uri: window.location.pathname //当前页面的URI，不包含问号后面的参数
    };


    /** ================ 全局初始化 ================ **/

    var _base_init = function () {
        if (debug === true) {
            k.log('Request ' + kvman.uri);
        }
        //Tooltip初始化
        $('[data-toggle="tooltip"]').tooltip();
    };

    var _global = {
        R: function () {
            var _r = {};
            for (var item in route) {
                if (route[item].hasOwnProperty('uri')) {
                    _r[route[item].uri] = route[item].init;
                }
            }
            return _r;
        },
        init: function () {
            //全局初始化
            _base_init();
            //基于页面的初始化
            var routes = this.R();
            if (routes.hasOwnProperty(kvman.uri)) {
                routes[kvman.uri](); //init for route
            }
        }
    };

    _global.init(); //初始化
});