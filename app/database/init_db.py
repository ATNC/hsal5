from .db import get_db_connection


def init_db():
    with get_db_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS currency (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        currency_code TEXT NOT NULL,
                        value REAL NOT NULL,
                        date TEXT NOT NULL)''')
        conn.commit()
