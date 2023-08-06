from PyQt5.QtWidgets import QMessageBox


class AlertDialog(QMessageBox):
    """
    显示一些必须的提示信息给用户
    """
    @staticmethod
    def alert(msg_content):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(msg_content)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
        return retval
