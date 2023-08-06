import logging
import random
import sys
from logging.config import fileConfig
import  base64
from PyQt5 import QtCore, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QApplication, QLabel, QLineEdit, QDesktopWidget, QHBoxLayout)

from PyQt5.QtWidgets import QGridLayout

from kiteprotocol.kite_protocol import KiteProtocol



class Captcha(QLabel):
    LOGGER = logging.getLogger()
    """
    图片验证码，点击可以刷新，能够被调用刷新
    """
    def __init__(self, parent, protocol:KiteProtocol, width=100, height=30):
        """
        parent: 父widget
        """
        super(Captcha, self).__init__()
        self.parent = parent
        self.protocol = protocol
        self.captcha_id = None
        self.__show_loading_captcha()
        self.__get_captcha(callback=self.__captcha_callback)
        self.is_getting_captcha = False # 是否已经在获取验证码，如果是则拒绝多次点击

    def mousePressEvent(self, QMouseEvent): # real signature unknown; restored from __doc__
        """ mousePressEvent(self, QMouseEvent) """
        self.__show_loading_captcha()

    def __show_loading_captcha(self):
        self.setPixmap(QPixmap("../img/captcha_loading.png"))
        self.setAlignment(Qt.Qt.AlignCenter)

    def mouseReleaseEvent(self, QMouseEvent):
        """

        """
        if not self.is_getting_captcha:
            self.LOGGER.info("mouse clicked")
            self.__get_captcha(self.__captcha_callback)
        else:
            self.LOGGER.info("mouse clicked, but ignored")

    def __captcha_callback(self, captcha_id, img_base64):
        self.captcha_id = captcha_id
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(img_base64))
        self.setPixmap(pixmap)
        self.setFixedWidth(pixmap.width())
        self.setFixedHeight(pixmap.height())
        self.is_getting_captcha = False

    def refresh(self):
        self.mouseReleaseEvent(None)

    def get_captcha_id(self):
        return self.captcha_id

    def __get_captcha(self, callback):
        """

        """
        self.is_getting_captcha = True
        self.protocol.get_captcha(callback)


class CaptchaWidget(QWidget):
    """

    """
    def __init__(self, parent, protocol):
        super(CaptchaWidget, self).__init__()
        self.parent = parent
        self.input = QLineEdit()
        self.captcha = Captcha(self, protocol)

        layout = QHBoxLayout()
        layout.addWidget(self.captcha)
        layout.addWidget(self.input)
        self.setLayout(layout)

    def get_captcha_val(self):
        return self.captcha.get_captcha_id(), self.input.text()

    def refresh(self):
        self.captcha.refresh()


if __name__=="__main__":
    fileConfig("../logging.ini")
    logger = logging.getLogger()
    app = QApplication(sys.argv)
    c = CaptchaWidget(None, KiteProtocol('../config.ini'))
    c.show()

    sys.exit(app.exec_())
