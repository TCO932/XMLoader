from PyQt6.QtWidgets import QApplication
from appUI import Ui_MainWindow
from PyQt6 import QtWidgets, QtGui
import os

os.environ['connection_str'] = ''
os.environ['table_name'] = ''
app = QApplication([])
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.setWindowIcon(QtGui.QIcon('xml_icon.svg'))
MainWindow.show()
app.exec()