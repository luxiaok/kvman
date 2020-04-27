/**
 * Kvm-Man
 * Powered By Luxiaok
 * https://github.com/luxiaok/kvman
 * */

/* Icon图标
 * 0 - 叹号
 * 1 - 打勾
 * 2 - 打叉
 * 3 - 问号
 * 4 - 锁
 * 5 - 难过
 * 6 - Smile
 * */

/******** Base Modules ********/

const k = {
    get_time: function () {
        let _date = new Date(),
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
        const now = '[' + this.get_time() + ']';
        console.log(now, logs);
    },
    random: function (len) {
        if (!len) len = 8; //默认长度
        let _org_num = Math.random();
        if (_org_num < 0.1) len++; //解决0.0xxxx导致生成随机数位数不足问题
        let len_num = Math.pow(10, len);
        return parseInt(_org_num * len_num);
    }
};


/***********  Route Modules ***********/

/* 虚拟机开机 */
const guest_start = function (name, status) {
    let msg = '您确定要将虚拟机 ' + name + ' 开机吗？';
    if (status === 1) {
        layer.alert('该虚拟机已是开机状态！', {title: '开机提示', icon: 0});
        return false;
    }
    layer.confirm(msg, {icon: 3, title: '开机提示'}, function (index) {
        $.ajax({
            type: "POST",
            url: "/guest/start",
            data: {name: name},
            dataType: "json",
            success: function (resp) {
                let code = resp['code'],
                    msg = resp['msg'];
                if (code === 0) {
                    layer.close(index);
                    layer.msg(msg);
                    location.reload();
                } else if (code < 0) {
                    layer.close(index);
                    layer.msg(msg);
                } else {
                    layer.close(index);
                    layer.alert('开机失败，请稍后再试！', {title: '开机提示', icon: 0});
                }
            },
            error: function () {
                layer.close(index);
                layer.alert('系统繁忙，请稍后再试！', {title: '开机提示', icon: 2});
            }
        });
    });
};

/* 虚拟机关机 */
const guest_shutdown = function (name, status) {
    let msg = '您确定要将虚拟机 ' + name + ' 关机吗？';
    if (status === 0) {
        layer.alert('该虚拟机已是关机状态！', {title: '关机提示', icon: 0});
        return false;
    }
    layer.confirm(msg, {icon: 3, title: '关机提示'}, function (index) {
        $.ajax({
            type: "POST",
            url: "/guest/shutdown",
            data: {name: name, force: 'no'},
            dataType: "json",
            success: function (resp) {
                let code = resp['code'],
                    msg = resp['msg'];
                if (code === 0) {
                    layer.close(index);
                    layer.msg(msg);
                    location.reload();
                } else if (code < 0) {
                    layer.close(index);
                    layer.msg(msg);
                } else {
                    layer.close(index);
                    layer.alert('关机失败，请稍后再试！', {title: '关机提示', icon: 0});
                }
            },
            error: function () {
                layer.close(index);
                layer.alert('系统繁忙，请稍后再试！', {title: '关机提示', icon: 2});
            }
        });
    });
};

/* 虚拟机重启 */
const guest_reboot = function (name, status) {
    let msg = '您确定要将虚拟机 ' + name + ' 重启吗？';
    if (status === 0) {
        layer.alert('该虚拟机暂未开机！', {title: '重启提示', icon: 0});
        return false;
    }
    layer.confirm(msg, {icon: 3, title: '重启提示'}, function (index) {
        layer.msg('正在重启……');
        layer.close(index);
    });
};

/* 自动启动 */
const guest_autostart = function (name, autostart) {
    let msg, flag;
    if (autostart === 0) {
        msg = '您确定要将虚拟机 ' + name + ' 设置为自动启动吗？';
        flag = 1;
    } else {
        msg = '您确定取消虚拟机 ' + name + ' 的自动启动吗？';
        flag = 0;
    }
    layer.confirm(msg, {icon: 3, title: '操作提示'}, function (index) {
        $.ajax({
            type: "POST",
            url: "/guest/autostart",
            data: {name: name, flag: flag},
            dataType: "json",
            success: function (resp) {
                let code = resp['code'],
                    msg = resp['msg'];
                if (code === 0) {
                    layer.close(index);
                    layer.msg(msg);
                    location.reload();
                } else if (code < 0) {
                    layer.close(index);
                    layer.msg(msg);
                } else {
                    layer.close(index);
                    layer.alert('设置失败，请稍后再试！', {title: 'KvMan提示', icon: 0});
                }
            },
            error: function () {
                layer.close(index);
                layer.alert('系统繁忙，请稍后再试！', {title: 'KvMan提示', icon: 2});
            }
        });
    });
};

/* 远程连接 */
const guest_console = function (name, status) {
    if (status !== 1) {
        layer.alert('该主机未开机，无法连接！', {title: '远程连接提示', icon: 2});
        return false;
    }
    $.ajax({
        type: "POST",
        url: "/guest/console",
        data: {guest: name},
        dataType: "json",
        success: function (resp) {
            let code = resp['code'],
                msg = resp['msg'];
            if (code === 0) {
                let url = '/guest/console?uuid=' + resp['data']['uuid'] + '&token=' + resp['data']['token'];
                window.open(url);
            } else if (code < 0) {
                layer.msg(msg);
            } else {
                layer.alert('获取远程连接失败，请稍后再试！', {title: 'KvMan提示', icon: 0});
            }
        },
        error: function () {
            layer.alert('系统繁忙，请稍后再试！', {title: 'KvMan提示', icon: 2});
        }
    });
};

/* 销毁虚拟机 */
const guest_destroy = function (name, status) {
    let msg = '您确定要将虚拟机 ' + name + ' 彻底销毁吗？';
    if (status === 1) {
        layer.alert('请先将虚拟机关闭！', {title: '销毁提示', icon: 0});
        return false;
    }
    layer.confirm(msg, {icon: 3, title: '销毁提示'}, function (index) {
        layer.msg('正在销毁……');
        layer.close(index);
    });
};

/************ 路由表 ************/

const route = {};

route.hello = function(){
    log('hello')
};

route.Index = {
    uri: '/',
    init: function () {
        k.log('Welcome to Kvman Dashboard center!');
    }
};

route.Guest = {
    uri: '/guest',
    init: function () {
        //开机
        $('.start-btn').click(function () {
            let name = $(this).data('name'),
                status = $(this).data('status');
            guest_start(name,status);
        });

        //关机
        $('.halt-btn').click(function () {
            let name = $(this).data('name'),
                status = $(this).data('status');
            guest_shutdown(name,status);
        });

        //重启
        $('.reboot-btn').click(function () {
            let name = $(this).data('name'),
                status = $(this).data('status');
            guest_reboot(name,status);
        });

        //自动启动
        $('.autostart-btn').click(function () {
            let name = $(this).data('name'),
                autostart = $(this).data('autostart');
            guest_autostart(name,autostart);
        });

        //远程连接
        $('.console-btn').click(function () {
            let name = $(this).data('name'),
                status = $(this).data('status');
            guest_console(name,status);
        });

        //销毁虚拟机
        $('.destroy-btn').click(function () {
            let name = $(this).val().trim(),
                status = $(this).data('status');
            guest_destroy(name,status);
        });
    }
};

route.GuestDetail = {
    uri: '/guest/detail',
    init: function () {
        //开机
        $('#startBtn').click(function () {
            let name = $('#name').val().trim(),
                status = $('#name').data('status');
            guest_start(name,status);
        });

        //关机
        $('#haltBtn').click(function () {
            let name = $('#name').val().trim(),
                status = $('#name').data('status');
            guest_shutdown(name,status);
        });

        //重启
        $('#rebootBtn').click(function () {
            let name = $('#name').val().trim(),
                status = $('#name').data('status');
            guest_reboot(name,status);
        });

        //远程连接
        $('#consoleBtn').click(function () {
            let name = $('#name').val().trim(),
                status = $('#name').data('status');
            guest_console(name,status);
        });

        //销毁虚拟机
        $('#destroyBtn').click(function () {
            let name = $('#name').val().trim(),
                status = $('#name').data('status');
            guest_destroy(name,status);
        });

        //查看配置文件
        $('#viewConfigBtn').click(function () {
            $('#xml_box').toggle();
        });

        //编辑配置
        $('#editBtn').click(function () {
            layer.msg('暂不支持编辑配置！');
        });
    }
};

route.Server = {
    uri: '/server',
    init: function () {
        //新增
        $('#add_kvm_btn').click(function () {
            $('#dialog_title').html('新增KVM服务器');
            $('#edit_dialog').modal();
            $('#hostname').val('');
            $('#protocol').val('');
            $('#port').val('');
            $('#username').val('');
            $('#password').val('');
            $('#parameters').val('');
            $('#comments').val('');
            $('#saveBtn').data('hostname', '');
        });

        //编辑
        $('.edit-btn').click(function () {
            let id = $(this).data('id'),
                hostname = $('#hostname_' + id).html().trim(),
                protocol = $('#protocol_' + id).html().trim(),
                port = $('#port_' + id).html().trim(),
                username = $('#username_' + id).html().trim(),
                password = $('#username_' + id).data('password'),
                parameters = $('#protocol_' + id).data('parameters'),
                comments = $('#comments_' + id).html().trim();
            $('#dialog_title').html('编辑KVM主机：' + hostname);
            $('#edit_dialog').modal();
            $('#hostname').val(hostname);
            $('#protocol').val(protocol);
            $('#port').val(port);
            $('#username').val(username);
            $('#password').val(password);
            $('#parameters').val(parameters);
            $('#comments').val(comments);
            $('#saveBtn').data('hostname', hostname);
        });

        //保存
        $('#saveBtn').click(function () {
            let hostname0 = $('#saveBtn').data('hostname'),
                hostname = $('#hostname').val().trim(),
                protocol = $('#protocol').val().trim(),
                port = $('#port').val().trim(),
                username = $('#username').val().trim(),
                password = $('#password').val().trim(),
                parameters = $('#parameters').val().trim(),
                comments = $('#comments').val().trim(),
                api = hostname0 === '' ? 'create' : 'update';
            $.ajax({
                type: "POST",
                url: "/server/" + api,
                data: {hostname0: hostname0, hostname: hostname, protocol: protocol, port: port, username: username, password: password, parameters: parameters, comments: comments},
                dataType: "json",
                success: function (resp) {
                    let code = resp['code'],
                        msg = resp['msg'];
                    if (code === 0) {
                        layer.msg(msg);
                        location.reload();
                    } else if (code < 0) {
                        layer.msg(msg);
                    } else {
                        layer.alert('保存失败，请稍后再试！', {title: 'KvMan提示', icon: 0});
                    }
                },
                error: function () {
                    layer.alert('系统繁忙，请稍后再试！', {title: 'KvMan提示', icon: 2});
                }
            });
        });

        //删除
        $('.delete-btn').click(function () {
            let id = $(this).data('id'),
                hostname = $('#hostname_' + id).html();
            layer.confirm('您确认要删除 ' + hostname + ' 吗？', {icon: 3, title: '删除提示'}, function (index) {
                $.ajax({
                    type: "POST",
                    url: "/server/delete",
                    data: {hostname: hostname},
                    dataType: "json",
                    success: function (resp) {
                        let code = resp['code'],
                            msg = resp['msg'];
                        if (code === 0) {
                            $('#row_' + id).slideUp("slow", function () {
                                $(this).remove();
                            });
                            layer.close(index);
                            layer.msg(msg);
                        } else if (code < 0) {
                            layer.close(index);
                            layer.msg(msg);
                        } else {
                            layer.close(index);
                            layer.alert('删除失败，请稍后再试！', {title: 'KvMan提示', icon: 0});
                        }
                    },
                    error: function () {
                        layer.close(index);
                        layer.alert('系统繁忙，请稍后再试！', {title: 'KvMan提示', icon: 2});
                    }
                });
            });
        });
    }
};

route.Setting = {
    uri: '/setting',
    init: function () {
        //保存
        $('#saveBtn').click(function () {
            let nickname = $('#nickname').val().trim(),
                username = $('#username').val().trim(),
                email = $('#email').val().trim();
            if (nickname === '') {
                layer.msg('请输入昵称！');
                $('#nickname').focus();
                return false;
            }
            if (username === '') {
                layer.msg('请输入用户名！');
                $('#username').focus();
                return false;
            }
            $.ajax({
                type: "POST",
                url: "/user/profile",
                data: {username: username, nickname: nickname, email: email},
                dataType: "json",
                success: function (resp) {
                    let code = resp['code'],
                        msg = resp['msg'];
                    if (code === 0) {
                        layer.msg(msg);
                    } else if (code < 0) {
                        layer.msg(msg);
                    } else {
                        layer.alert('保存失败，请稍后再试！', {title: 'KvMan提示', icon: 0});
                    }
                },
                error: function () {
                    layer.alert('系统繁忙，请稍后再试！', {title: 'KvMan提示', icon: 2});
                }
            });
        });
    }
};

route.Install = {
    uri: '/setting/install',
    init: function () {
        //保存
        $('#saveBtn').click(function () {
            let nickname = $('#nickname').val().trim(),
                username = $('#username').val().trim(),
                password = $('#password').val().trim(),
                password2 = $('#password2').val().trim();
            if (nickname === '') {
                layer.msg('请输入昵称！');
                $('#nickname').focus();
                return false;
            }
            if (username === '') {
                layer.msg('请输入用户名！');
                $('#username').focus();
                return false;
            }
            if (password === '') {
                layer.msg('请输入登录密码！');
                $('#password').focus();
                return false;
            }
            if (password2 === '') {
                layer.msg('请再次输入登录密码！');
                $('#password2').focus();
                return false;
            }
            if (password !== password2) {
                layer.msg('两次密码输入不一致，请重新输入！');
                $('#password').val('');
                $('#password2').val('');
                $('#password').focus();
                return false;
            }
            $.ajax({
                type: "POST",
                url: "/setting/install",
                data: {username: username, nickname: nickname, password: password, password2: password2},
                dataType: "json",
                success: function (resp) {
                    let code = resp['code'],
                        msg = resp['msg'];
                    if (code === 0) {
                        layer.alert(msg, {title: '安装成功提示', icon: 1}, function (index) {
                            layer.close(index);
                            location.href = '/user/login?_from=install'; //跳转登录页面
                        });
                    } else if (code < 0) {
                        layer.msg(msg);
                    } else {
                        layer.alert('保存失败，请检查您的部署环境！', {title: 'KvMan提示', icon: 0});
                    }
                },
                error: function () {
                    layer.alert('系统错误，请检查您的部署环境！', {title: 'KvMan提示', icon: 2});
                }
            });
        });
    }
};

route.Passwd = {
    uri: '/user/passwd',
    init: function () {
        //保存
        $('#passwdBtn').click(function () {
            let password0 = $('#password0').val().trim(),
                password = $('#password').val().trim(),
                password2 = $('#password2').val().trim();
            if (password0 === '') {
                layer.msg('请输入原始密码！');
                $('#password0').focus();
                return false;
            }
            if (password === '') {
                layer.msg('请输入新密码！');
                $('#password').focus();
                return false;
            }
            if (password2 === '') {
                layer.msg('请再次输入新密码！');
                $('#password2').focus();
                return false;
            }
            if (password0 === password) {
                layer.msg('新旧密码相同，请重新输入！');
                $('#password0').val('');
                $('#password').val('');
                $('#password2').val('');
                $('#password0').focus();
                return false;
            }
            if (password !== password2) {
                layer.msg('两次新密码输入不一致，请重新输入！');
                $('#password').val('');
                $('#password2').val('');
                $('#password').focus();
                return false;
            }
            $.ajax({
                type: "POST",
                url: "/user/passwd",
                data: {password0: password0, password: password, password2: password2},
                dataType: "json",
                success: function (resp) {
                    let code = resp['code'],
                        msg = resp['msg'];
                    if (code === 0) {
                        layer.alert(msg, {title: '密码修改提示', icon: 1});
                        $('#password0').val('');
                        $('#password').val('');
                        $('#password2').val('');
                    } else if (code < 0) {
                        layer.msg(msg);
                    } else {
                        layer.alert('修改密码失败，请稍后再试！', {title: 'KvMan提示', icon: 0});
                    }
                },
                error: function () {
                    layer.alert('系统繁忙，请稍后再试！', {title: 'KvMan提示', icon: 2});
                }
            });
        });
    }
};

route.Login = {
    uri: '/user/login',
    init: function () {
        //登录
        $('#login_btn').click(function () {
            let username = $('#username').val().trim(),
                password = $('#password').val().trim();
            if (username === '') {
                layer.alert('请输入用户名！', {title: '登录提示', icon: 2}, function (index) {
                    layer.close(index);
                    $('#username').focus();
                });
                return false;
            }
            if (password === '') {
                layer.alert('请输入密码！', {title: '登录提示', icon: 2}, function (index) {
                    layer.close(index);
                    $('#password').focus();
                });
                return false;
            }
            let loading = layer.load(1, {shade: [0.4, '#000']});
            $.ajax({
                type: "POST",
                url: "/user/login",
                data: {username: username, password: password},
                dataType: "json",
                success: function (resp) {
                    let code = resp['code'],
                        msg = resp['msg'];
                    layer.close(loading);
                    if (code === 0) {
                        //layer.msg(msg);
                        location.href = $('#login_btn').data('next'); //跳转到登录前的页面
                    } else if (code < 0) {
                        layer.msg(msg);
                    } else {
                        layer.alert('登录失败，请稍后再试！', {title: '登录提示', icon: 0}); //icon = !
                    }
                },
                error: function () {
                    layer.close(loading);
                    layer.alert('系统繁忙，请稍后再试！', {title: '登录提示', icon: 2}); // icon = x
                }
            });
        });
    }
};


/********** 导出方法 **********/

//export default function(){
//    k.log('Invoke Default');
//}

export { k, route };