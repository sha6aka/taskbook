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
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        query_db_create()
        query_messages_add()


# Создание БД
def query_db_create():
    try:
        # tlist - id, номер заявки, статус архивности, дата создания, дата последнего обновления
        # tdata - id, номер заявки, текст, дата создания записи
        # messages - id, код сообщения, текст сообщения
        cursor.executescript("""CREATE TABLE tlist (
                                _id integer primary key autoincrement,
                                tasknum integer not null unique,
                                archive integer,
                                date datetime default current_timestamp,
                                last_update datetime default current_timestamp);

                                CREATE TABLE tdata (
                                _id integer primary key autoincrement,
                                tasknum integer not null,
                                text char(512),
                                date datetime default current_timestamp);
                                
                                CREATE TABLE messages (
                                _id integer primary key autoincrement,
                                msgcode char(20) not null,
                                msgtext char(512));""")
    except sqlite3.DatabaseError as e:
        message(e.args[0])
    except sqlite3.Error as e:
        message(e.args[0])
    else:
        conn.commit()


# Заполнение таблицы сообщений
def query_messages_add():
    dct = {
        # Работа с заявками
        "error_1": "Пустой номер заявки",
        "error_2": "Выберите заявку для удаления",
        "error_5": "Выберите заявку для архивации/разархивации",
        # Работа с данными заявки
        "error_3": "Введите текст по заявке",
        "error_4": "Выберите заявку"
    }
    for key, value in dct.items():
            cursor.execute("INSERT INTO messages (msgcode, msgtext) VALUES ('{}', '{}');".format(key, value))
            conn.commit()


# Создание заявки
def query_create_task(tasknum):
    try:
        cursor.execute("INSERT INTO tlist (tasknum, archive, date, last_update) "
                       "VALUES ({}, 0, datetime('now', 'localtime'), datetime('now', 'localtime'));".format(tasknum))
        cursor.execute("INSERT INTO tdata (tasknum, text, date) "
                       "VALUES ({}, \"Заявка добавлена\", datetime('now', 'localtime'))".format(tasknum))
    except sqlite3.DatabaseError as e:
        message(e.args[0])
    else:
        conn.commit()


# Удаление заявки
def query_delete_task(tasknum):
    try:
        cursor.execute("DELETE FROM tlist WHERE tasknum = {};".format(tasknum))
        cursor.execute("DELETE FROM tdata WHERE tasknum = {};".format(tasknum))
    except sqlite3.DatabaseError as e:
        message(e.args[0])
    else:
        conn.commit()


# Проверка архивности заявки
def query_check_arch(tasknum):
    try:
        arch = cursor.execute("SELECT archive FROM tlist WHERE tasknum = {};".format(tasknum)).fetchone()
    except sqlite3.DatabaseError as e:
        message(e.args[0])
    else:
        return arch[0]


# Архивация/разархивация заявки
def query_arch_unarch(tasknum, code, text):
    try:
        cursor.execute("""UPDATE tlist SET archive = ? WHERE tasknum = ?;""", (code, tasknum))
        cursor.execute("""INSERT INTO tdata (tasknum, text, date)
                          VALUES (?, ?, datetime('now', 'localtime'));""", (tasknum, text))
        cursor.execute("""UPDATE tlist
                          SET last_update = datetime('now', 'localtime')
                          WHERE tasknum = {};""".format(tasknum))
    except sqlite3.DatabaseError as e:
        message(e.args[0])
    else:
        conn.commit()


# Получение/обновление списка заявок
def query_tlist_getlist(ident, arch):
    try:
        a = cursor.execute("SELECT tasknum FROM tlist WHERE archive = ? ORDER BY ? DESC;", (arch, ident))
    except sqlite3.DatabaseError as e:
        message(e.args[0])
    else:
        return a


# Получение данных о заявке
def query_tdata_get(tasknum):
    try:
        a = cursor.execute("""SELECT _id, text, strftime('%d.%m.%Y   %H:%M:%S', date)
                              FROM tdata WHERE tasknum = {} ORDER BY date;""".format(tasknum))
    except sqlite3.DatabaseError as e:
        message(e.args[0])
    else:
        return a


# Добавление данных в заявку
def query_tdata_add(tasknum, text):
    try:
        cursor.execute("""INSERT INTO tdata (tasknum, text, date)
                          VALUES ({}, '{}', datetime('now', 'localtime'));""".format(tasknum, text))
        cursor.execute("""UPDATE tlist
                          SET last_update = datetime('now', 'localtime')
                          WHERE tasknum = {};""".format(tasknum))
    except sqlite3.DatabaseError as e:
        message(e.args[0])
    else:
        conn.commit()


# Удаление данных из заявки
def query_tdata_delete(taskid):
    try:
        cursor.execute("DELETE FROM tdata WHERE _id = {}".format(taskid))
    except sqlite3.DatabaseError as e:
        message(e.args[0])
    else:
        conn.commit()


# Окно с сообщениями
def message(err):
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Сообщение об ошибке")
    msg = cursor.execute("SELECT msgtext FROM messages WHERE msgcode = '{}';".format(err)).fetchone()
    if msg is not None:
        msgBox.setText("Ошибка: " + msg[0])
    else:
        msgBox.setText("Ошибка: " + err)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()
