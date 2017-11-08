import os
import sqlite3
from PyQt5.QtWidgets import QMessageBox


# Подключение к БД
def db_connect():
    db = "db.sqlite"
    global conn, cursor
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
    else:
        # tasks - id, номер заявки, статус архивности, дата создания, дата последнего обновления
        # taskdata - id, номер заявки, текст, дата создания записи
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        query_db_create()


# Создание БД
def query_db_create():
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
    else:
        conn.commit()


# Создание заявки
def query_create_task(tasknum):
    try:
        cursor.execute("INSERT INTO tasks (tasknum, archive, date, last_update) "
                       "VALUES ({}, 0, datetime('now', 'localtime'), datetime('now', 'localtime'));".format(tasknum))
        cursor.execute("INSERT INTO taskdata (tasknum, text, date) "
                       "VALUES ({}, \"Заявка добавлена\", datetime('now', 'localtime'))".format(tasknum))
    except sqlite3.DatabaseError as e:
        error_msg(e.args[0])
    else:
        conn.commit()


# Удаление заявки
def query_delete_task(tasknum):
    try:
        cursor.execute("DELETE FROM tasks WHERE tasknum = {};".format(tasknum))
        cursor.execute("DELETE FROM taskdata WHERE tasknum = {};".format(tasknum))
    except sqlite3.DatabaseError as e:
        error_msg(e.args[0])
    else:
        conn.commit()


# Проверка архивности заявки
def query_check_arch(tasknum):
    try:
        arch = cursor.execute("SELECT archive FROM tasks WHERE tasknum = {};".format(tasknum)).fetchone()
    except sqlite3.DatabaseError as e:
        error_msg(e.args[0])
    else:
        return arch[0]


# Архивация/разархивация заявки
def query_arch_unarch(tasknum, code, text):
    try:
        cursor.execute("""UPDATE tasks SET archive = ? WHERE tasknum = ?;""", (code, tasknum))
        cursor.execute("""INSERT INTO taskdata (tasknum, text, date)
                          VALUES (?, ?, datetime('now', 'localtime'));""", (tasknum, text))
        cursor.execute("""UPDATE tasks
                          SET last_update = datetime('now', 'localtime')
                          WHERE tasknum = {};""".format(tasknum))
    except sqlite3.DatabaseError as e:
        error_msg(e.args[0])
    else:
        conn.commit()


# Получение/обновление списка заявок
def query_tasks_list(ident, arch):
    try:
        a = cursor.execute("SELECT tasknum FROM tasks WHERE archive = ? ORDER BY ? DESC;", (arch, ident))
    except sqlite3.DatabaseError as e:
        error_msg(e.args[0])
    else:
        return a


# Получение данных о заявке
def query_taskdata_get(tasknum):
    try:
        a = cursor.execute("""SELECT _id, text, strftime('%d.%m.%Y   %H:%M:%S', date)
                              FROM taskdata WHERE tasknum = {} ORDER BY date;""".format(tasknum))
    except sqlite3.DatabaseError as e:
        error_msg(e.args[0])
    else:
        return a


# Добавление данных в заявку
def query_taskdata_add(tasknum, text):
    try:
        cursor.execute("""INSERT INTO taskdata (tasknum, text, date)
                          VALUES ({}, '{}', datetime('now', 'localtime'));""".format(tasknum, text))
        cursor.execute("""UPDATE tasks
                          SET last_update = datetime('now', 'localtime')
                          WHERE tasknum = {};""".format(tasknum))
    except sqlite3.DatabaseError as e:
        error_msg(e.args[0])
    else:
        conn.commit()


# Удаление данных из заявки
def query_taskdata_delete(taskid):
    try:
        cursor.execute("DELETE FROM taskdata WHERE _id = {}".format(taskid))
    except sqlite3.DatabaseError as e:
        error_msg(e.args[0])
    else:
        conn.commit()


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
