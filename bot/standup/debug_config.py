from standup.config import BASE_DIR

# Build paths inside the project like this: BASE_DIR / 'subdir'.

DB_DIR = BASE_DIR / 'debug_standups.db'
OUT_FILE_DIR = BASE_DIR / 'debug.out'

STANDUP_TIME = '2338'
STANDUP_DAYS = [1, 3, 5, 6, 7]

DB_TABLES = {
    "standup": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "update_date datetime",
            "username TEXT NOT NULL",
            "block TEXT NOT NULL",
            "doing TEXT NOT NULL",
            "did TEXT NOT NULL"
        ]
    },
    "users": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "user_id INTEGER NOT NULL",
            "chat_id INTEGER NOT NULL",
            "username TEXT NOT NULL"
        ]
    }
}
