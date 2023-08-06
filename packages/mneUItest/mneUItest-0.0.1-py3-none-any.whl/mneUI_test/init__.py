import sys
from GUI import MainWindow
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
