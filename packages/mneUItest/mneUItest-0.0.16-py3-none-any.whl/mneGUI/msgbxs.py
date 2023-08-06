from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget


def alert_msg(window, title, msg):
    alert = QMessageBox(window)
    alert.setWindowTitle(title)
    alert.setText(msg)
    alert.exec_()

#test
# import sys
# app = QApplication(sys.argv)
# main_window = QWidget()
# main_window.show()
# QMessageBox(main_window, "Alert", "message")
# sys.exit(app.exec_())
