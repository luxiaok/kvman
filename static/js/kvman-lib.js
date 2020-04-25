/**
 * Kvm-Man
 * Powered By Luxiaok
 * https://github.com/luxiaok/kvman
 * */

//export default function(){
//    console.log('Call default');
//}

/******** Base Module ********/

export const k = {
    get_time: function () {
        var _date = new Date(),
            year = _date.getFullYear(),
            month = _date.getMonth() + 1, //注意：getMonth返回的数据是0-11
            day = _date.getDate(),
            hours = _date.getHours(),
            minutes = _date.getMinutes(),
            seconds = _date.getSeconds();
        month = month < 10 ? '0' + month : month;
        day = day < 10 ? '0' + day : day;
        hours = hours < 10 ? '0' + hours : hours;
        minutes = minutes < 10 ? '0' + minutes : minutes;
        seconds = seconds < 10 ? '0' + seconds : seconds;
        return year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds;
    },
    log: function (logs) {
        var now = '[' + this.get_time() + ']';
        console.log(now, logs);
    },
    random: function (len) {
        if (!len) len = 8; //默认长度
        var _org_num = Math.random();
        if (_org_num < 0.1) len++; //解决0.0xxxx导致生成随机数位数不足问题
        var len_num = Math.pow(10, len);
        return parseInt(_org_num * len_num);
    }
};

/***********  Route ***********/

export const route = {};

route.hello = function(){
    log('hello')
};

route.Index = {
    uri: '/',
    init: function () {
        k.log('Welcome to Kvman Dashboard center!');
    }
};
