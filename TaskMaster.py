# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QRegExp, QRect, Qt
from PyQt5.QtWidgets import *
import db


class Ui_MainWindow(object):

    def __init__(self):
        self.centralwidget = QWidget(MainWindow)

        self.button_Addtdata = QPushButton(self.centralwidget)
        self.button_Deletetdata = QPushButton(self.centralwidget)
        self.field_Addtdata = QTextEdit(self.centralwidget)
        self.view_tdata = QTableWidget(self.centralwidget)
        self.group_CurrentTlist = QGroupBox(self.centralwidget)
        self.group_Work = QGroupBox(self.centralwidget)

        self.button_AddTask = QPushButton(self.group_Work)
        self.button_DeleteTask = QPushButton(self.group_Work)
        self.button_ArchiveTask = QPushButton(self.group_Work)
        self.button_Sort = QComboBox(self.group_Work)
        self.field_NewTaskNumber = QLineEdit(self.group_Work)
        self.list_CurrentTlist = QListWidget(self.group_CurrentTlist)

        self.menuBar = QMenuBar(MainWindow)
        self.menu = QMenu(self.menuBar)
        self.button_Changelog = QAction(MainWindow)

    def setupUi(self, MainWindow):
        # Стартовое окно
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 600))
        MainWindow.setMaximumSize(QtCore.QSize(1024, 600))
        MainWindow.setBaseSize(QtCore.QSize(1024, 600))
        MainWindow.setWindowTitle("TaskMaster v0.4")
        self.centralwidget.setObjectName("centralwidget")

        # Таблица данных по заявке
        self.view_tdata.setGeometry(QRect(210, 10, 801, 471))
        self.view_tdata.setObjectName("view_tdata")
        self.view_tdata.setColumnCount(3)
        self.view_tdata.setColumnWidth(0, 0)
        self.view_tdata.setColumnWidth(1, 662)
        self.view_tdata.setColumnWidth(2, 120)
        self.view_tdata.hideColumn(0)
        self.view_tdata.setRowCount(0)
        self.view_tdata.verticalHeader().hide()
        item = QTableWidgetItem()
        self.view_tdata.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.view_tdata.setHorizontalHeaderItem(2, item)
        # добавить фиксированную ширину столбцов
        # добавить автоматическое увеличение в высоту под весь текст
        # сделать поля нередактируемыми

        # Группа работы с заявками
        self.group_Work.setGeometry(QtCore.QRect(10, 10, 191, 100))
        self.group_Work.setObjectName("group_Work")
        self.field_NewTaskNumber.setGeometry(QRect(0, 20, 191, 20))
        self.field_NewTaskNumber.setAlignment(Qt.AlignCenter)
        self.field_NewTaskNumber.setValidator(QtGui.QRegExpValidator(QRegExp("[0-9]+")))  # ограничение на ввод только цифр
        self.field_NewTaskNumber.setMaxLength(8)  # ограничение по количеству текста
        self.field_NewTaskNumber.setObjectName("field_NewTaskNumber")
        self.button_AddTask.setGeometry(QRect(0, 50, 90, 20))
        self.button_AddTask.setObjectName("button_AddTask")
        self.button_DeleteTask.setGeometry(QRect(100, 50, 90, 20))
        self.button_DeleteTask.setObjectName("button_DeleteTask")
        self.button_ArchiveTask.setGeometry(QtCore.QRect(0, 80, 90, 20))
        self.button_ArchiveTask.setObjectName("button_ArchiveTask")
        self.button_Sort.setGeometry(QtCore.QRect(100, 80, 90, 20))
        self.button_Sort.setObjectName("button_Sort")
        self.button_Sort.addItem("")
        self.button_Sort.addItem("")
        self.button_Sort.addItem("")
        self.button_Sort.addItem("")

        # Текущие и архивные заявки
        self.group_CurrentTlist.setGeometry(QRect(10, 116, 190, 456))
        self.group_CurrentTlist.setObjectName("group_CurrentTlist")
        self.list_CurrentTlist.setGeometry(QRect(0, 16, 190, 439))
        self.list_CurrentTlist.setObjectName("list_CurrentTlist")

        # Добавление и работа с данными по заявке
        self.field_Addtdata.setGeometry(QRect(210, 490, 701, 81))
        self.field_Addtdata.setObjectName("field_Addtdata")
        self.button_Addtdata.setGeometry(QRect(924, 520, 91, 51))
        self.button_Addtdata.setObjectName("button_Addtdata")
        self.button_Deletetdata.setGeometry(QRect(924, 490, 91, 21))
        self.button_Deletetdata.setObjectName("button_Deletetdata")

        # Меню
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuBar.addAction(self.menu.menuAction())
        self.menu.setObjectName("menu")
        self.menu.addAction(self.button_Changelog)
        MainWindow.setMenuBar(self.menuBar)
        self.button_Changelog.setObjectName("button_Changelog")

        # Нажатия на кнопку
        self.button_AddTask.clicked.connect(self.create_task)
        self.button_DeleteTask.clicked.connect(self.delete_task)
        self.list_CurrentTlist.clicked.connect(self.get_task_data)
        self.button_Addtdata.clicked.connect(self.add_task_data)
        self.button_ArchiveTask.clicked.connect(self.button_archive_task)

        # Остальное
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.get_task_list("tasknum")
        self.list_CurrentTlist.setCurrentRow(0)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.view_tdata.horizontalHeaderItem(1).setText(_translate("MainWindow", "Текст заметки"))
        self.view_tdata.horizontalHeaderItem(2).setText(_translate("MainWindow", "Дата и время"))
        self.button_Addtdata.setText(_translate("MainWindow", "Добавить\nзапись"))
        self.button_Deletetdata.setText(_translate("MainWindow", "Удалить запись"))
        self.group_CurrentTlist.setTitle(_translate("MainWindow", "Список заявок"))
        self.button_AddTask.setText(_translate("MainWindow", "Добавить"))
        self.button_DeleteTask.setText(_translate("MainWindow", "Удалить"))
        self.button_ArchiveTask.setText(_translate("MainWindow", "В/из архива"))
        self.button_Sort.setItemText(0, _translate("MainWindow", "Сортировка"))
        self.button_Sort.setItemText(1, _translate("MainWindow", "Возрастание"))
        self.button_Sort.setItemText(2, _translate("MainWindow", "Убывание"))
        self.button_Sort.setItemText(3, _translate("MainWindow", "Last Update"))
        self.group_Work.setTitle(_translate("MainWindow", "Работа с заявками"))
        self.menu.setTitle(_translate("MainWindow", "Other"))
        self.button_Changelog.setText(_translate("MainWindow", "Changelog"))

    # Создание заявки
    def create_task(self):
        tasknum = self.field_NewTaskNumber.text()
        if tasknum == "" or None:
            db.message("error_1")
        else:
            db.query_create_task(tasknum)
            self.field_NewTaskNumber.clear()
            self.get_task_list("tasknum")
            # добавить фокусировку на добавленном номере

    # Удаление заявки
    def delete_task(self):
        self.view_tdata.setRowCount(0)
        if self.list_CurrentTlist.currentItem() is not None:
            """Добавить вопрос "да/нет"
            msgBox_title = "Сообщение об ошибке"
            msgBox_text = "Предупреждение: Заявка будет удалена вместе со всеми данными. Продолжить?"
            msgBox_reply = QMessageBox.question(self, msgBox_title, msgBox_text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if msgBox_reply == QMessageBox.Yes:"""
            tasknum = self.list_CurrentTlist.currentItem().text()
            db.query_delete_task(tasknum)
            self.get_task_list("tasknum")
            # добавить фокусировку на 1й строке и проверку ее существования
            # self.list_CurrentTlist.setCurrentRow(0)
            # self.get_task_data()
        else:
            db.message("error_2")

    # Архивация заявок
    def button_archive_task(self):
        # Добавить вопрос "да/нет"
        self.view_tdata.setRowCount(0)
        if self.list_CurrentTlist.currentItem() is not None:
            tasknum = self.list_CurrentTlist.currentItem().text()
            arch = db.query_check_arch(tasknum)
            if arch == 0:
                db.query_arch_unarch(tasknum, 1, "Заявка добавлена в архив")
            else:
                db.query_arch_unarch(tasknum, 0, "Заявка убрана из архива")
            self.get_task_list("tasknum")
        else:
            db.message("error_5")

    # Получить/обновить список заявок
    def get_task_list(self, ident):
        self.list_CurrentTlist.clear()
        for elem in db.query_tlist_getlist(ident, 0):
            self.list_CurrentTlist.addItem(str(elem[0]))
        for elem in db.query_tlist_getlist(ident, 1):
            self.list_CurrentTlist.addItem(str(elem[0]))

    # Получить данные по заявке
    def get_task_data(self):
        self.view_tdata.setRowCount(0)
        if self.list_CurrentTlist.currentItem() is not None:
            tasknum = self.list_CurrentTlist.currentItem().text()
            for elem in db.query_tdata_get(tasknum):
                self.view_tdata.insertRow(0)
                self.view_tdata.setItem(0, 0, QTableWidgetItem(elem[0]))
                self.view_tdata.setItem(0, 1, QTableWidgetItem(elem[1]))
                self.view_tdata.setItem(0, 2, QTableWidgetItem(elem[2]))
                self.view_tdata.resizeRowToContents(0)
                # добавить фокусировку на первой записи

    # Добавить данные в заявку
    def add_task_data(self):
        if self.list_CurrentTlist.currentItem() is not None:
            tasknum = self.list_CurrentTlist.currentItem().text()
            text = self.field_Addtdata.toPlainText()
            if text != "" or None:
                db.query_tdata_add(tasknum, text)
                self.field_Addtdata.clear()
                self.get_task_data()
            else:
                db.message("error_3")
        else:
            db.message("error_4")

    # Удалить данные из заявки
    def delete_task_data(self):
        if self.view_tdata.selectedItems() is not None:
            taskid = self.view_tdata.rowAt()
            db.query_tdata_delete(taskid)
            self.get_task_data()
        else:
            db.message("error_4")


if __name__ == "__main__":
    import sys
    db.db_connect()
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
