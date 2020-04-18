/**
 * Kvm-Man
 * Powered By Luxiaok
 * https://github.com/luxiaok/kvman
 * */

$(function () {

    //绑定Tooltip
    $('[data-toggle="tooltip"]').tooltip();

    //定义Kvman全局变量
    kvman = {
        foo: 'bar'
    };


    //生成随机字符串
    kvman.random = function(len){
        if (!len) len = 8; //默认长度
        var _org_num = Math.random();
        if (_org_num<0.1) len++; //解决0.0xxxx导致生成随机数位数不足问题
        var len_num = Math.pow(10,len);
        return parseInt(_org_num*len_num);
    };
});