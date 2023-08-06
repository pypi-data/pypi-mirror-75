import logging
import sys
from logging.config import fileConfig
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QApplication, QLabel, QLineEdit, QDesktopWidget, QHBoxLayout)

from PyQt5.QtWidgets import QGridLayout

from kiteprotocol.kite_protocol import KiteProtocol
from uilib.alert_msg_dialog import AlertDialog
from uilib.captcha_form import CaptchaWidget


class LoginForm(QWidget):
    LOGGER = logging.getLogger()
    """
    登录界面
    """
    def __init__(self, parent, protocol:KiteProtocol):
        super().__init__()
        self.parent = parent
        self.protocol = protocol
        self.grid_layout = QGridLayout()

        self.user_label = QLabel('用户名')
        self.user_input  = QLineEdit()
        self.psw_label = QLabel('密码')
        self.psw_input = QLineEdit()
        self.psw_input.setEchoMode(QLineEdit.Password)
        self.captcha_widget = CaptchaWidget(self, protocol)
        self.login_btn = QPushButton("登录")

        self.init_ui()

    def init_ui(self):
        self.grid_layout.addWidget(self.user_label, 1,0)
        self.grid_layout.addWidget(self.user_input, 1,1)
        self.grid_layout.addWidget(self.psw_label, 2,0)
        self.grid_layout.addWidget(self.psw_input, 2,1)
        self.grid_layout.addWidget(self.captcha_widget, 3, 1) # 验证码

        self.grid_layout.addWidget(self.login_btn, 4,1)
        self.setLayout(self.grid_layout)
        self.__center()

        self.setWindowTitle('请登录')
        self.login_btn.clicked.connect(self.__do_login)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

    def __center(self):
        self.setGeometry(300, 300, 300,150)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __do_login(self):
        self.login_btn.setEnabled(False)
        self.LOGGER.info("login clicked")
        user= self.user_input.text()
        psw = self.psw_input.text()
        captcha_id, captcha_val = self.captcha_widget.get_captcha_val()
        succ, err, token = self.__login(user, psw, captcha_val, captcha_id)
        if succ:
            self.LOGGER.info("login ok")
            self.protocol.open()
            # self.close()
            self.parent.show()
        else:
            self.LOGGER.info("user = %s, psw=%s, captcha=%s", user, psw, captcha_val)
            self.LOGGER.info("login error, retry")
            AlertDialog.alert(err)
            self.captcha_widget.refresh()
            self.login_btn.setEnabled(True)

    def __login(self, user, psw, captcha, captcha_id):
        """

        :param user:
        :param psw:
        :param captchar:
        :return:
        """
        succ, err, auth_token = self.protocol.login(user, psw, captcha, captcha_id)
        self.LOGGER.info(f"login: {succ}, {err}, {auth_token}")
        return succ, err, auth_token


if __name__=="__main__":
    fileConfig("../logging.ini")
    logger = logging.getLogger()
    app = QApplication(sys.argv)
    f = LoginForm(None, KiteProtocol('../config.ini'))
    f.show()
    sys.exit(app.exec_())
