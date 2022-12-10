import sqlite3
from logging import info as print
from standup.config import DEBUG 

if DEBUG:
    import standup.debug_config as BotConfig
else:
    import standup.production_config as BotConfig


def check_table(name):
    ans = []
    try:
        sqlite_connection = sqlite3.connect(BotConfig.DB_DIR)
        sqlite_check_table_query = f"SELECT * FROM sqlite_master WHERE type='table' AND name='{name}'" 
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_check_table_query)
        ans = cursor.fetchall()
        sqlite_connection.commit()
        print("Таблица SQLite проверена")
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return bool(ans)

def create_table(columns, name):
    try:
        sqlite_connection = sqlite3.connect(BotConfig.DB_DIR)
        sqlite_create_table_query = 'CREATE TABLE ' + name + ' (' + ', '.join(map(str, columns)) + ');'
        # sqlite_create_table_query = '''CREATE TABLE sqlitedb_developers (
        #                             id INTEGER PRIMARY KEY,
        #                             name TEXT NOT NULL,
        #                             email text NOT NULL UNIQUE,
        #                             joining_date datetime,
        #                             salary REAL NOT NULL);'''

        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица SQLite создана")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return 0

def create_row(row, table_name, columns_name: str):
    try:
        sqlite_connection = sqlite3.connect(BotConfig.DB_DIR)
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        q = ('?, ' * len(row))[:-2]
        cursor.execute(f"INSERT INTO {table_name} {columns_name} VALUES({q});", row)
        sqlite_connection.commit()
        print("Строчка SQLite создана")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return 0

def find_row(table_name, value, column_name):
    ans = False
    try:
        sqlite_connection = sqlite3.connect(BotConfig.DB_DIR)
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} LIKE {value}")
        ans = bool(cursor.fetchall())
        print("Sql запрос выполнен успешно")
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    except UnboundLocalError as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return ans

def get_tables():
    ...
    
def get_rows(table):
    ...
    
def get_columns(table):
    ...