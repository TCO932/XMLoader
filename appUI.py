# Form implementation generated from reading ui file 'app.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from db import DB
from tableModel import TableModel
from xml.etree import ElementTree as ET
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1097, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1097, 600))
        MainWindow.setMaximumSize(QtCore.QSize(1097, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.chooseFile = QtWidgets.QPushButton(self.centralwidget)
        self.chooseFile.setGeometry(QtCore.QRect(20, 20, 241, 31))
        self.chooseFile.setMinimumSize(QtCore.QSize(241, 31))
        self.chooseFile.setMaximumSize(QtCore.QSize(241, 31))
        self.chooseFile.setObjectName("chooseFile")
        self.loadFile = QtWidgets.QPushButton(self.centralwidget)
        self.loadFile.setGeometry(QtCore.QRect(20, 60, 241, 31))
        self.loadFile.setMinimumSize(QtCore.QSize(241, 31))
        self.loadFile.setMaximumSize(QtCore.QSize(241, 31))
        self.loadFile.setObjectName("loadFile")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(20, 140, 241, 431))
        self.tableView.setMinimumSize(QtCore.QSize(241, 431))
        self.tableView.setMaximumSize(QtCore.QSize(241, 431))
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setVisible(False)
        self.tableView.horizontalHeader().setDefaultSectionSize(241)
        self.tableView.setObjectName("tableView")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(270, 20, 821, 551))
        self.plainTextEdit.setMinimumSize(QtCore.QSize(821, 551))
        self.plainTextEdit.setMaximumSize(QtCore.QSize(821, 551))
        # self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 100, 241, 31))
        self.lineEdit.setMinimumSize(QtCore.QSize(241, 31))
        self.lineEdit.setMaximumSize(QtCore.QSize(241, 31))
        self.lineEdit.setObjectName("lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.addFunctions()
        self.getTableData()

    def getTableData(self):
        data = self.db.selectAll()
        self.tableView.setModel(TableModel(data))
        self.tableView.setColumnHidden(1, True);


    def addFunctions(self):
        self.db = DB(os.environ['connection_str'], os.environ['table_name'])

        self.chooseFile.clicked.connect(self.chooseFileButtonOnClick)
        self.loadFile.clicked.connect(self.loadFileButtonOnClick)
        self.tableView.clicked.connect(self.tableRowOnClick)
        self.tableView.clicked.connect(self.tableRowOnClick)

    def tableRowOnClick(self, index):
        nameIndex = self.tableView.model().index(index.row(), 0)
        self.file_name = self.tableView.model().data(nameIndex, QtCore.Qt.ItemDataRole.DisplayRole)
        idIndex = self.tableView.model().index(index.row(), 1)
        self.file_id = self.tableView.model().data(idIndex, QtCore.Qt.ItemDataRole.DisplayRole)

        result = self.db.selectById(self.file_id)
        self.plainTextEdit.setPlainText(result[0])
        # print(result)

    def chooseFileButtonOnClick(self):
        self.file_id = None
        self.lineEdit.setText('')
        self.file_path = QtWidgets.QFileDialog.getOpenFileName(filter="xml(*.xml)")[0]
        if not self.file_path == "":
            file=open(self.file_path, "r")
            content = file.read()
            self.plainTextEdit.setPlainText(content)
            file.close()

    # def delete(self):
    #     self.file_id = None
    #     self.lineEdit.setText('')
    #     self.file_path = QtWidgets.QFileDialog.getOpenFileName(filter="xml(*.xml)")[0]
    #     if not self.file_path == "":
    #         file=open(self.file_path, "r")
    #         content = file.read()
    #         self.plainTextEdit.setPlainText(content)
    #         file.close()

    def validateXML(self, xml):
        x = ET.fromstring(xml)

    def loadFileButtonOnClick(self):
        self.file_name = self.lineEdit.text()
        if (not self.file_name.replace(" ", "")):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Внимание')
            msg.setWindowIcon(QtGui.QIcon('xml_icon.svg'))
            msg.setText('Введите название файла')
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            retval = msg.exec()
            return
        # print(self.file_name)
        try:
            if (self.file_id):
                content = self.plainTextEdit.toPlainText()
                self.validateXML(content)
                self.db.update(self.file_id, self.file_name, content)
                self.getTableData()
                return
            if (hasattr(self, 'file_path') and self.file_path):
                file=open(self.file_path, "r")
                content = file.read()
                self.validateXML(content)
                self.db.insert(self.file_name, content)
                self.getTableData()
                return
        except ET.ParseError as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Ошибка')
            msg.setWindowIcon(QtGui.QIcon('xml_icon.svg'))
            msg.setText('Неверный формат xml документа')
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            retval = msg.exec()
            # print(e)
        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Ошибка')
            msg.setText(str(e))
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            retval = msg.exec()
            # print(e)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Загрузить XML"))
        self.chooseFile.setText(_translate("MainWindow", "Выбрать файл"))
        self.loadFile.setText(_translate("MainWindow", "Сохранить файл"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Введите название файла"))