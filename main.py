# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QRegExp, QRect
from PyQt5.QtWidgets import *
import sqlite3
import os


class Ui_MainWindow(object):
    def __init__(self):
        self.centralWidget = QWidget(MainWindow)
        self.removeTextBtn = QPushButton(self.centralWidget)
        self.addTextBtn = QPushButton(self.centralWidget)
        self.addDataArea = QTextEdit(self.centralWidget)
        self.taskData = QTableWidget(self.centralWidget)

        self.currentTaskBox = QGroupBox(self.centralWidget)
        self.deleteTaskBtn = QPushButton(self.currentTaskBox)
        self.addTaskBtn = QPushButton(self.currentTaskBox)
        self.addTaskText = QLineEdit(self.currentTaskBox)
        self.currentTasks = QListWidget(self.currentTaskBox)

        self.menuBar = QMenuBar(MainWindow)
        self.menuTestt = QMenu(self.menuBar)

    def setupUi(self, MainWindow):
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
        MainWindow.setWindowTitle("TaskMaster v0.1")

        self.centralWidget.setObjectName("centralwidget")

        self.taskData.setGeometry(QRect(210, 10, 805, 471))
        self.taskData.setObjectName("taskData")
        self.taskData.setColumnCount(3)
        self.taskData.setColumnWidth(0, 0)
        self.taskData.setColumnWidth(1, 666)
        self.taskData.setColumnWidth(2, 120)
        self.taskData.hideColumn(0)
        self.taskData.setRowCount(0)
        self.taskData.verticalHeader().hide()
        item = QTableWidgetItem()
        self.taskData.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.taskData.setHorizontalHeaderItem(2, item)
        # добавить фиксированную ширину столбцов
        # добавить автоматическое увеличение в высоту под весь текст
        # сделать поля нередактируемыми

        self.addDataArea.setGeometry(QRect(210, 490, 705, 81))
        self.addDataArea.setObjectName("addDataArea")

        self.addTextBtn.setGeometry(QRect(924, 520, 91, 51))
        self.addTextBtn.setObjectName("addDataBtn")

        self.removeTextBtn.setGeometry(QRect(924, 490, 91, 25))
        self.removeTextBtn.setObjectName("removeDataBtn")

        self.currentTaskBox.setGeometry(QRect(10, 10, 191, 561))
        self.currentTaskBox.setObjectName("currentTaskBox")

        self.currentTasks.setGeometry(QRect(0, 80, 191, 481))
        self.currentTasks.setObjectName("currentTasks")

        self.addTaskText.setGeometry(QRect(10, 20, 171, 20))
        self.addTaskText.setAlignment(QtCore.Qt.AlignCenter)
        self.addTaskText.setValidator(QtGui.QRegExpValidator(QRegExp("[0-9]+"), self.addTaskText))  # ограничение на ввод только цифр
        self.addTaskText.setMaxLength(9)  # ограничение по количеству текста
        self.addTaskText.setObjectName("addTaskText")

        self.addTaskBtn.setGeometry(QRect(10, 50, 81, 21))
        self.addTaskBtn.setObjectName("addTaskBtn")

        self.deleteTaskBtn.setGeometry(QRect(100, 50, 81, 21))
        self.deleteTaskBtn.setObjectName("deleteTaskBtn")

        self.menuBar.setGeometry(QRect(0, 0, 1024, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuTestt.setObjectName("menuTestt")
        MainWindow.setMenuBar(self.menuBar)
        self.menuBar.addAction(self.menuTestt.menuAction())

        self.addTaskBtn.clicked.connect(self.create_task)
        self.deleteTaskBtn.clicked.connect(self.delete_task)
        self.currentTasks.clicked.connect(self.get_task_data)
        self.addTextBtn.clicked.connect(self.add_task_data)

        MainWindow.setCentralWidget(self.centralWidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.get_task_list()
        self.currentTasks.setCurrentRow(0)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.taskData.horizontalHeaderItem(1).setText(_translate("MainWindow", "Текст"))
        self.taskData.horizontalHeaderItem(2).setText(_translate("MainWindow", "Дата и время"))
        self.addTextBtn.setText(_translate("MainWindow", "Добавить\nзапись"))
        self.removeTextBtn.setText(_translate("MainWindow", "Удалить запись"))
        self.currentTaskBox.setTitle(_translate("MainWindow", "Список заявок"))
        self.addTaskBtn.setText(_translate("MainWindow", "Добавить"))
        self.deleteTaskBtn.setText(_translate("MainWindow", "Удалить"))
        self.menuTestt.setTitle(_translate("MainWindow", "testt"))

    # Создание заявки
    def create_task(self):
        task = self.addTaskText.text()
        if task == "" or None:
            error_msg("Пустой номер заявки.")
        else:
            try:
                cursor.execute("INSERT INTO tasks (tasknum, archive, date, last_update) "
                               "VALUES ({}, 0, datetime('now', 'localtime'), datetime('now', 'localtime'));".format(task))
                cursor.execute("INSERT INTO taskdata (tasknum, text, date) "
                               "VALUES ({}, \"Заявка добавлена\", datetime('now', 'localtime'))".format(task))
            except sqlite3.DatabaseError as e:
                error_msg(e.args[0])
            else:
                conn.commit()
                self.addTaskText.clear()
                self.get_task_list()
                # добавить фокусировку на добавленном номере

    # Удаление заявки
    def delete_task(self):
        # Добавить вопрос "да/нет"
        self.taskData.setRowCount(0)
        if self.currentTasks.currentItem() is not None:
            task = self.currentTasks.currentItem().text()
            try:
                cursor.execute("DELETE FROM tasks WHERE tasknum = {};".format(task))
                cursor.execute("DELETE FROM taskdata WHERE tasknum = {};".format(task))
            except sqlite3.DatabaseError as e:
                error_msg(e.args[0])
            else:
                conn.commit()
                self.get_task_list()
                # добавить фокусировку на 1й строке и проверку ее существования
                # self.currentTasks.setCurrentRow(0)
                # self.get_task_data()
        else:
            error_msg("Выберите заявку для удаления.")

    # Получить/обновить список заявок
    def get_task_list(self):
        self.currentTasks.clear()
        try:
            a = cursor.execute("SELECT tasknum FROM tasks ORDER BY last_update DESC;")
        except sqlite3.DatabaseError as e:
            error_msg(e.args[0])
        else:
            for elem in a:
                self.currentTasks.addItem(str(elem[0]))

    # Получить данные по заявке
    def get_task_data(self):
        self.taskData.setRowCount(0)
        try:
            task = self.currentTasks.currentItem().text()
            a = cursor.execute("SELECT _id, text, strftime('%d.%m.%Y   %H:%M:%S', date) FROM taskdata WHERE tasknum = {} ORDER BY date;".format(task))
        except sqlite3.DatabaseError as e:
            error_msg(e.args[0])
        else:
            for elem in a:
                self.set_text_area(elem[0], elem[1], elem[2])
                # добавить фокусировку на первой записи

    # Формирование строки в поле с данными
    def set_text_area(self, elemid, elemtext, elemtime):
        self.taskData.insertRow(0)
        self.taskData.resizeRowToContents(0)
        self.taskData.setItem(0, 0, QTableWidgetItem(elemid))
        self.taskData.setItem(0, 1, QTableWidgetItem(elemtext))
        self.taskData.setItem(0, 2, QTableWidgetItem(elemtime))

    # Добавить данные в заявку
    def add_task_data(self):
        if self.currentTasks.currentItem() != "" or None:
            task = self.currentTasks.currentItem().text()
            text = self.addDataArea.toPlainText()
            if text != "" or None:
                try:
                    cursor.execute("""INSERT INTO taskdata (tasknum, text, date)
                                      VALUES ({}, '{}', datetime('now', 'localtime'));""".format(task, text))
                    cursor.execute("""UPDATE tasks
                                      SET last_update = datetime('now', 'localtime')
                                      where tasknum = {};""".format(task))
                except sqlite3.DatabaseError as e:
                    error_msg(e.args[0])
                else:
                    conn.commit()
                    self.addDataArea.clear()
                    self.get_task_data()
            else:
                error_msg("Введите текст по заявке.")
        else:
            error_msg("Выберите заявку.")

    # Удалить данные из заявки
    def delete_task_data(self):
        try:
            error_msg(self.taskData.currentRow())
            taskid = self.taskData.QTableWidgetItem(self.taskData.currentRow(), 3)
            error_msg(taskid)
            cursor.execute("DELETE FROM taskdata WHERE _id = {}".format(taskid))
            conn.commit()
        except sqlite3.DatabaseError as e:
            error_msg(e.args[0])


# Окно с ошибками
def error_msg(e):
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Сообщение об ошибке")
    msgBox.setText("Ошибка: " + e)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()


# Подключение/создание к БД
def connect_db():
    global conn, cursor
    db = "db.sqlite"
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
    else:
        # tasks - id, номер заявки, статус архивности, дата создания, дата последнего обновления
        # taskdata - id, номер заявки, текст, дата создания записи
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            cursor.executescript("""create table tasks (
                                    _id integer primary key autoincrement,
                                    tasknum integer not null unique,
                                    archive boolean,
                                    date datetime default current_timestamp,
                                    last_update datetime default current_timestamp);

                                    create table taskdata (
                                    _id integer primary key autoincrement,
                                    tasknum integer not null,
                                    text char(512),
                                    date datetime default current_timestamp);""")
        except sqlite3.DatabaseError as e:
            error_msg(e.args[0])
        except sqlite3.Error as e:
            error_msg(e.args[0])
        except os.error as e:
            error_msg(e.args[0])
        else:
            conn.commit()


if __name__ == "__main__":
    import sys
    connect_db()
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
