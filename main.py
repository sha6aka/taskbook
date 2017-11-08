# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QRegExp, QRect, Qt
from PyQt5.QtWidgets import *
import sqlite3
import os


class Ui_MainWindow(object):
    def __init__(self):
        self.centralwidget = QWidget(MainWindow)

        self.button_AddTaskData = QPushButton(self.centralwidget)
        self.button_DeleteTaskData = QPushButton(self.centralwidget)
        self.field_AddTaskData = QTextEdit(self.centralwidget)
        self.view_TaskData = QTableWidget(self.centralwidget)
        self.group_CurrentTasks = QGroupBox(self.centralwidget)
        self.group_Work = QGroupBox(self.centralwidget)

        self.button_AddTask = QPushButton(self.group_Work)
        self.button_DeleteTask = QPushButton(self.group_Work)
        self.button_ArchiveTask = QPushButton(self.group_Work)
        self.button_Sort = QComboBox(self.group_Work)
        self.field_NewTaskNumber = QLineEdit(self.group_Work)
        self.list_CurrentTasks = QListWidget(self.group_CurrentTasks)

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
        MainWindow.setWindowTitle("TaskMaster v0.2")
        self.centralwidget.setObjectName("centralwidget")

        # Таблица данных по заявке
        self.view_TaskData.setGeometry(QRect(210, 10, 801, 471))
        self.view_TaskData.setObjectName("view_TaskData")
        self.view_TaskData.setColumnCount(3)
        self.view_TaskData.setColumnWidth(0, 0)
        self.view_TaskData.setColumnWidth(1, 662)
        self.view_TaskData.setColumnWidth(2, 120)
        self.view_TaskData.hideColumn(0)
        self.view_TaskData.setRowCount(0)
        self.view_TaskData.verticalHeader().hide()
        item = QTableWidgetItem()
        self.view_TaskData.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.view_TaskData.setHorizontalHeaderItem(2, item)
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
        self.group_CurrentTasks.setGeometry(QRect(10, 116, 190, 456))
        self.group_CurrentTasks.setObjectName("group_CurrentTasks")
        self.list_CurrentTasks.setGeometry(QRect(0, 16, 190, 439))
        self.list_CurrentTasks.setObjectName("list_CurrentTasks")

        # Добавление и работа с данными по заявке
        self.field_AddTaskData.setGeometry(QRect(210, 490, 701, 81))
        self.field_AddTaskData.setObjectName("field_AddTaskData")
        self.button_AddTaskData.setGeometry(QRect(924, 520, 91, 51))
        self.button_AddTaskData.setObjectName("button_AddTaskData")
        self.button_DeleteTaskData.setGeometry(QRect(924, 490, 91, 21))
        self.button_DeleteTaskData.setObjectName("button_DeleteTaskData")

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
        self.list_CurrentTasks.clicked.connect(self.get_task_data)
        self.button_AddTaskData.clicked.connect(self.add_task_data)
        self.button_ArchiveTask.clicked.connect(self.button_archive_task)

        # Остальное
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.get_task_list("tasknum")
        self.list_CurrentTasks.setCurrentRow(0)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.view_TaskData.horizontalHeaderItem(1).setText(_translate("MainWindow", "Текст заметки"))
        self.view_TaskData.horizontalHeaderItem(2).setText(_translate("MainWindow", "Дата и время"))
        self.button_AddTaskData.setText(_translate("MainWindow", "Добавить\nзапись"))
        self.button_DeleteTaskData.setText(_translate("MainWindow", "Удалить запись"))
        self.group_CurrentTasks.setTitle(_translate("MainWindow", "Список заявок"))
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
        task = self.field_NewTaskNumber.text()
        if task == "" or None:
            error_msg("error_1")
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
                self.field_NewTaskNumber.clear()
                self.get_task_list("tasknum")
                # добавить фокусировку на добавленном номере

    # Удаление заявки
    def delete_task(self):
        self.view_TaskData.setRowCount(0)
        if self.list_CurrentTasks.currentItem() is not None:
            """Добавить вопрос "да/нет"
            msgBox_title = "Сообщение об ошибке"
            msgBox_text = "Предупреждение: Заявка будет удалена вместе со всеми данными. Продолжить?"
            msgBox_reply = QMessageBox.question(self, msgBox_title, msgBox_text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if msgBox_reply == QMessageBox.Yes:"""
            task = self.list_CurrentTasks.currentItem().text()
            try:
                cursor.execute("DELETE FROM tasks WHERE tasknum = {};".format(task))
                cursor.execute("DELETE FROM taskdata WHERE tasknum = {};".format(task))
            except sqlite3.DatabaseError as e:
                error_msg(e.args[0])
            else:
                conn.commit()
                self.get_task_list("tasknum")
                # добавить фокусировку на 1й строке и проверку ее существования
                # self.list_CurrentTasks.setCurrentRow(0)
                # self.get_task_data()
        else:
            error_msg("error_2")

    # Архивация заявок
    def button_archive_task(self):
        # Добавить вопрос "да/нет"
        self.view_TaskData.setRowCount(0)
        if self.list_CurrentTasks.currentItem() is not None:
            task = self.list_CurrentTasks.currentItem().text()
            try:
                arch = cursor.execute("SELECT archive FROM tasks WHERE tasknum = {};".format(task)).fetchone()
                self.db_archive_task(task, arch[0])
            except sqlite3.DatabaseError as e:
                error_msg(e.args[0])
            else:
                self.get_task_list("tasknum")
        else:
            error_msg("error_5")

    def db_archive_task(self, task, archive):
        if archive == 0:
            text = "Заявка добавлена в архив"
            code = 1
        else:
            text = "Заявка убрана из архива"
            code = 0
        try:
            cursor.execute("""UPDATE tasks SET archive = ? WHERE tasknum = ?;""", (code, task))
            cursor.execute("""INSERT INTO taskdata (tasknum, text, date)
                              VALUES (?, ?, datetime('now', 'localtime'));""", (task, text))
            cursor.execute("""UPDATE tasks
                              SET last_update = datetime('now', 'localtime')
                              WHERE tasknum = {};""".format(task))
        except sqlite3.DatabaseError as e:
            error_msg(e.args[0])
        else:
            conn.commit()

    # Получить/обновить список заявок
    def get_task_list(self, ident):
        self.list_CurrentTasks.clear()
        try:
            a = cursor.execute("SELECT tasknum FROM tasks WHERE archive = 0 ORDER BY {} DESC;".format(ident))
        except sqlite3.DatabaseError as e:
            error_msg(e.args[0])
        else:
            for elem in a:
                self.list_CurrentTasks.addItem(str(elem[0]))
        try:
            a = cursor.execute("SELECT tasknum FROM tasks WHERE archive = 1 ORDER BY {} DESC;".format(ident))
        except sqlite3.DatabaseError as e:
            error_msg(e.args[0])
        else:
            for elem in a:
                self.list_CurrentTasks.addItem(str(elem[0]))

    # Получить данные по заявке
    def get_task_data(self):
        self.view_TaskData.setRowCount(0)
        if self.list_CurrentTasks.currentItem() is not None:
            task = self.list_CurrentTasks.currentItem().text()
            try:
                a = cursor.execute("""SELECT _id, text, strftime('%d.%m.%Y   %H:%M:%S', date)
                                      FROM taskdata WHERE tasknum = {} ORDER BY date;""".format(task))
            except sqlite3.DatabaseError as e:
                error_msg(e.args[0])
            else:
                for elem in a:
                    self.set_text_area(elem[0], elem[1], elem[2])
                    # добавить фокусировку на первой записи

    # Формирование строки в поле с данными
    def set_text_area(self, elemid, elemtext, elemtime):
        self.view_TaskData.insertRow(0)
        self.view_TaskData.setItem(0, 0, QTableWidgetItem(elemid))
        self.view_TaskData.setItem(0, 1, QTableWidgetItem(elemtext))
        self.view_TaskData.setItem(0, 2, QTableWidgetItem(elemtime))
        self.view_TaskData.resizeRowToContents(0)

    # Добавить данные в заявку
    def add_task_data(self):
        if self.list_CurrentTasks.currentItem() is not None:
            task = self.list_CurrentTasks.currentItem().text()
            text = self.field_AddTaskData.toPlainText()
            if text != "" or None:
                try:
                    cursor.execute("""INSERT INTO taskdata (tasknum, text, date)
                                      VALUES ({}, '{}', datetime('now', 'localtime'));""".format(task, text))
                    cursor.execute("""UPDATE tasks
                                      SET last_update = datetime('now', 'localtime')
                                      WHERE tasknum = {};""".format(task))
                except sqlite3.DatabaseError as e:
                    error_msg(e.args[0])
                else:
                    conn.commit()
                    self.field_AddTaskData.clear()
                    self.get_task_data()
            else:
                error_msg("error_3")
        else:
            error_msg("error_4")

    # Удалить данные из заявки
    def delete_task_data(self):
        try:
            error_msg(self.view_TaskData.currentRow())
            taskid = self.view_TaskData.QTableWidgetItem(self.view_TaskData.currentRow(), 1)
            error_msg(taskid)
            cursor.execute("DELETE FROM taskdata WHERE _id = {}".format(taskid))
            conn.commit()
        except sqlite3.DatabaseError as e:
            error_msg(e.args[0])


# Окно с ошибками
def error_msg(e):
    dct = {
        # Работа с заявками
        "error_1": "Пустой номер заявки",
        "error_2": "Выберите заявку для удаления",
        "error_5": "Выберите заявку для архивации/разархивации",
        # Работа с данными заявки
        "error_3": "Введите текст по заявке",
        "error_4": "Выберите заявку"
    }
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Сообщение об ошибке")
    if dct.get(e) is not None:
        msgBox.setText("Ошибка: " + dct[e])
    else:
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
            cursor.executescript("""CREATE TABLE tasks (
                                    _id integer primary key autoincrement,
                                    tasknum integer not null unique,
                                    archive integer,
                                    date datetime default current_timestamp,
                                    last_update datetime default current_timestamp);

                                    CREATE TABLE taskdata (
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
