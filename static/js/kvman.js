/**
 * Kvm-Man
 * Powered By Luxiaok
 * https://github.com/luxiaok/kvman
 * */

import { k,route } from './kvman-lib.js?_v=20.4.26.2';

$(function () {

    const debug = true;

    const kvman = {
        foo: 'bar',
        uri: window.location.pathname //当前页面的URI，不包含问号后面的参数
    };


    /** ================ 全局初始化 ================ **/

    const _base_init = function () {
        if (debug === true) {
            k.log('Request ' + kvman.uri);
        }
        //Tooltip初始化
        $('[data-toggle="tooltip"]').tooltip();
    };

    const _global = {
        get_routes: function () {
            let _r = {}, i;
            for (i in route) {
                if (route[i].hasOwnProperty('uri')) {
                    _r[route[i].uri] = route[i];
                }
            }
            return _r;
        },
        init: function () {
            //全局初始化
            _base_init();
            //基于页面的初始化
            const routes = this.get_routes();
            if (routes.hasOwnProperty(kvman.uri)) {
                routes[kvman.uri].init(); //init for current route
            }
        }
    };

    _global.init(); //初始化
});