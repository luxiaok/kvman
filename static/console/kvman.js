/**
 * Kvm-Man
 * Powered By Luxiaok
 * https://github.com/luxiaok/kvman
 * */

// RFB holds the API to connect and communicate with a VNC server
import RFB from './core/rfb.js';

const init = function () {
    let rfb, desktopName;

    // When this function is called we have successfully connected to a server
    function connectedToServer(e) {
        status("已连接 " + desktopName);
        document.getElementById('status').style.color = '#fff';
    }

    // This function is called when we are disconnected
    function disconnectedFromServer(e) {
        document.getElementById('status').style.color = 'yellow';
        if (e.detail.clean) {
            status("已断开连接");
        } else {
            status("请求出错，连接已断开");
        }
    }

    // When this function is called, the server requires credentials to authenticate
    function credentialsAreRequired(e) {
        const password = prompt("Password Required:");
        rfb.sendCredentials({password: password});
    }

    // When this function is called we have received a desktop name from the server
    function updateDesktopName(e) {
        desktopName = e.detail.name;
    }

    // Since most operating systems will catch Ctrl+Alt+Del before they get a chance to be intercepted by the browser,
    // we provide a way to emulate this key sequence.
    function sendCtrlAltDel() {
        layer.confirm('您确认要发送组合键 Ctrl + Alt + Del 吗？<br><span style="color:red;">提示：该操作将有可能导致设备重启！</span>', {icon: 3, title: '操作提示'}, function (index) {
            rfb.sendCtrlAltDel();
            layer.close(index);
            layer.msg('发送成功！');
        });
        return false;
    }

    // Show a status text in the top bar
    function status(text) {
        document.getElementById('status').textContent = text;
        console.log(text);
    }

    // This function extracts the value of one variable from the query string.
    // If the variable isn't defined in the URL it returns the default value instead.
    function readQueryVariable(name, defaultValue) {
        // A URL with a query parameter can look like this: https://www.example.com?myqueryparam=myvalue
        // Note that we use location.href instead of location.search because Firefox < 53 has a bug w.r.t location.search
        const re = new RegExp('.*[?&]' + name + '=([^&#]*)'),
            match = document.location.href.match(re);

        if (match) {
            // We have to decode the URL since want the cleartext value
            return decodeURIComponent(match[1]);
        }

        return defaultValue;
    }

    document.getElementById('sendCtrlAltDelButton').onclick = sendCtrlAltDel;

    // Read parameters specified in the URL query string
    const host = readQueryVariable('host', window.location.hostname);
    //let port = readQueryVariable('port', window.location.port);
    let port = document.getElementById('status').getAttribute('data-port');
    const password = readQueryVariable('password'),
          uuid = readQueryVariable('uuid', null),
          token = readQueryVariable('token', null),
          path = 'kvman?token=' + uuid + ':' + token;

    //Ready for connecting ...
    status("正在连接：");

    // Build the websocket URL used to connect
    let url;
    if (window.location.protocol === "https:") {
        url = 'wss';
    } else {
        url = 'ws';
    }
    url += '://' + host;
    if (port) {
        url += ':' + port;
    }
    url += '/' + path;

    // Creating a new RFB object will start a new connection
    rfb = new RFB(document.getElementById('screen'), url, {credentials: {password: password}});

    // Add listeners to important events from the RFB module
    rfb.addEventListener("connect", connectedToServer);
    rfb.addEventListener("disconnect", disconnectedFromServer);
    rfb.addEventListener("credentialsrequired", credentialsAreRequired);
    rfb.addEventListener("desktopname", updateDesktopName);

    // Set parameters that can be changed on an active connection
    rfb.viewOnly = readQueryVariable('view_only', false);
    rfb.scaleViewport = readQueryVariable('scale', false);
};

$(function () {
    /* 初始化 */
    init();
    /* 退出远程程控 */
    $('#exitBtn').click(function () {
        const uuid = $(this).data('uuid');
        layer.confirm('您确认退出远程控制吗？', {icon: 3, title: '退出提示'}, function (index) {
            $.ajax({
                type: "POST",
                url: "/guest/console-exit",
                data: {uuid: uuid},
                dataType: "json",
                success: function (resp) {
                    let code = resp['code'],
                        msg = resp['msg'];
                    if (code === 0) {
                        layer.close(index);
                        window.close(); //关闭当前窗口
                    } else if (code < 0) {
                        layer.close(index);
                        layer.msg(msg);
                    } else {
                        layer.close(index);
                        layer.alert('操作失败，请稍后再试！', {title: '操作提示', icon: 0});
                    }
                },
                error: function () {
                    layer.close(index);
                    layer.alert('系统繁忙，请稍后再试！', {title: '操作提示', icon: 2});
                }
            });
        });
    });
});