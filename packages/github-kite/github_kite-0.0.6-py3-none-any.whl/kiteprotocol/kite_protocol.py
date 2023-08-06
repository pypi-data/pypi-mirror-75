import configparser
import json
import sys
import time
from logging.config import fileConfig

import websocket

from concurrent.futures.thread import ThreadPoolExecutor

from kiteprotocol.utils import http_get, get_device_id, get_device_name, http_post
import uuid
import logging
import threading


class KiteProtocol(object):
    OK = 0
    ERR = 1
    PROTOCOL_VERSION = "0.1"
    A_LOGIN = "A_LOGIN"
    A_PULL_CONFIG = "A_PULL_CONFIG"
    A_RESET_AUTH_TOKEN = "A_RESET_AUTH_TOKEN" # 重置客户端auth_token
    A_CON_DENY = "A_CON_DENY" # 拒绝连接，参数不全
    A_AUTH_ERROR = "A_AUTH_ERROR"  # auth_token 不对
    A_BAD_PROTO = "A_BAD_PROTO" # json格式不对
    A_MSG_NOTIFY = "A_MSG_NOTIFY" # 发送到客户端的消息
    A_FORCE_OFFLINE = "A_FORCE_OFFLINE" # 强制客户端下线
    A_DEVICE_TOO_MANY = "A_DEVICE_TOO_MANY" # 同时在线设备超过设定数目

    LOGGER = logging.getLogger()
    executor = ThreadPoolExecutor(max_workers=1)

    def __init__(self, cfg_file):
        """
        初始化从编译时就固定的配置里获取实际的通信地址

        """
        self.login_url = None
        self.captcha_url = None
        self.wss_url = None
        self.wss = None  # websocke 连接
        self.auth_token = None
        self.device_id = self.__init_device_id()
        self.device_name = self.__init_device_name()
        self.__init(cfg_file)
        self.ws_thread = None
        self.ws_opend = False
        self.protocol_init = False

    def __init(self, cfg_file):
        """
        初始化服务地址
        """
        # TODO 优化: 实际通信地址缓存起来，如果出错再获取
        conf = configparser.ConfigParser()
        conf.read(cfg_file)
        meta_url = conf.get("metadata", "meta_url")
        # 然后从meta_url获取具体服务的地址
        j = http_get(meta_url)
        self.login_url, self.captcha_url, self.wss_url = j['login'], j['captcha'], j['ws_addr']

    def get_captcha(self, callback):
        """
            获取验证码图片
        """
        self.executor.submit(http_get, self.captcha_url, callback=callback)

    def login(self, user_name, psw, captcha, captcha_id):
        uid = str(uuid.uuid4())
        action = self.A_LOGIN
        device_id = self.device_id
        device_name = self.device_name

        jo = http_post(self.login_url, data={
            "uid": uid,
            "action": action,
            "username": user_name,
            "password": psw,
            "captcha": captcha,
            "captcha_id": captcha_id,
            "device_id": device_id,
            "device_name": device_name
        })
        self.LOGGER.info(jo)  # TODO jo is None
        self.auth_token = jo['auth_token']  # 保存着以后ws用
        return jo['code'] == 0, jo['err'], jo['auth_token']

    def open(self):
        websocket.enableTrace(True)
        self.wss = websocket.WebSocketApp(self.wss_url,
                                          on_message=self.on_message,
                                          on_error=self.on_error,
                                          on_close=self.on_close,
                                          on_open=self.on_open,
                                          cookie=f"auth_token={self.auth_token}; device_id={self.device_id}; device_name={self.device_name}")

        self.ws_thread = threading.Thread(target=self.wss.run_forever, name="kite_ws_client", daemon=True)
        self.ws_thread.start()  # 启动ws线程
        self.LOGGER.info("ws thread start")
        return self.wss

    def pull_cli_config(self):

        data = {
            "uid": str(uuid.uuid4()),
            "auth_token": self.auth_token,
            "protocol_version": self.PROTOCOL_VERSION,
            "action": self.A_PULL_CONFIG,
            "device_id": self.device_id
        }
        self.send_json(data=data)

    def send_json(self, data, to=10):
        while to > 0:
            if self.ws_opend and self.protocol_init:
                data['auth_token'] = self.auth_token  # 刷新
                self.wss.send(json.dumps(data))
                self.LOGGER.info("data SEND >> %s", data)
                break
            else:
                self.LOGGER.info("ws not opend")
                time.sleep(1)
            to = to - 1

    def on_message(self, message):
        self.LOGGER.info("ws receive %s", message)
        jso = json.loads(message)
        action = jso['action']
        if action == self.A_RESET_AUTH_TOKEN:
            self.__cb_reset_auth_token(jso)
        elif action == self.A_CON_DENY:
            self._cb_server_con_deny(jso)
        elif action == self.A_PULL_CONFIG:
            self._cb_pull_config(jso)
        elif action == self.A_AUTH_ERROR:
            self._cb_auth_error(jso)
        elif action == self.A_BAD_PROTO:
            self._cb_bad_proto(jso)
        elif action ==self.A_MSG_NOTIFY:
            self._cb_msg_notify(jso)
        elif action == self.A_FORCE_OFFLINE:
            self._cb_force_offline(jso)
        elif action == self.A_DEVICE_TOO_MANY:
            self._cb_device_too_much(jso)
        else:
            raise Exception("unimplemented")

    def __cb_reset_auth_token(self, jso):
        self.auth_token = jso['auth_token'] # TODO 持久化
        self.protocol_init = True
        self.LOGGER.info(f"auth token reset {self.auth_token}")

    def _cb_server_con_deny(self, jso, *args, **kwargs):
        """
        {"code":1, "err":message, 'action':"A_CON_DENY"}
        """
        raise Exception("_cb_server_con_deny() unimplemented")

    def _cb_pull_config(self, jso, *args, **kwargs):
        """
        {"uid": "b4560938-c3ad-479d-9cfa-91df5efd077a", "action": "A_PULL_CONFIG",
        "protocol_version": 0.1, "code": 0, "err": "",
        "service_info":
            {"code": 0, "data": true, "id": "f5bb9b60-bf8d-11ea-ab62-aaa604eb06fb",
            "ssport": 30000, "kcp_port": 30001, "kpsw":"abc124xxx", "sspsw": "gktebcna", "ip": "192.168.153.128"
            },
        "backup_service": {}, "extra_info": {}}
        """
        raise Exception("_cb_pull_config() unimplemented")

    def _cb_auth_error(self, jso, *args, **kwargs):
        """
        {"code": 1, "err": message, 'action': "A_AUTH_ERROR"}
        """
        raise Exception("_cb_auth_error() unimplemented")

    def _cb_bad_proto(self, jso, *args, **kwargs):
        """
        {"code":1, "err":"bad kiteprotocol format", "action":"A_BAD_PROTO", "raw":message}
        """
        raise Exception("_cb_bad_proto() unimplemented")

    def _cb_msg_notify(self, jso, *args, **kwargs):
        """

        """
        raise Exception("_cb_msg_notify() unimplemented")

    def _cb_force_offline(self, jso, *args, **kwargs):
        """

        """
        raise Exception("_cb_force_offline() unimplemented")

    def _cb_device_too_much(self, jso, *args, **kwargs):
        """

        """
        raise Exception("_cb_device_too_much() unimplemented")

    def on_error(self, message):
        self.LOGGER.info("ws error %s", message)
        self.ws_opend = False

    def on_close(self):
        self.LOGGER.info("ws closed")

    def on_open(self):
        self.LOGGER.info("ws OPEND!")
        self.ws_opend = True

    @staticmethod
    def __init_device_id():
        return get_device_id()

    @staticmethod
    def __init_device_name():
        return get_device_name()


if __name__ == "__main__":
    import os
    import sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from PyQt5.QtWidgets import QApplication
    from uilib.login_form import LoginForm

    cfg = "config.ini"
    kite_pro = KiteProtocol(cfg)


    class T:
        def show(self):
            print("login ok, parent show")
            # kite_pro.send_json({"message":"hahah", "int":111, "auth_token":kite_pro.auth_token, "uid":"1111@"})
            kite_pro.pull_cli_config()


    fileConfig("logging.ini")
    # logger = logging.getLogger()
    app = QApplication(sys.argv)
    f = LoginForm(T(), kite_pro)
    f.show()

    sys.exit(app.exec_())
