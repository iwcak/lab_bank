import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../db/bank.db")


class Database:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            pesel TEXT UNIQUE NOT NULL,
            account_number TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            balance REAL DEFAULT 0
        )
        """)
        self.conn.commit()

    def create_user(self, name, surname, pesel, account_number, password_hash):
        try:
            self.cursor.execute("""
            INSERT INTO users (name, surname, pesel, account_number, password_hash, balance)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (name, surname, pesel, account_number, password_hash, 0))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user_by_account(self, account_number):
        self.cursor.execute("""
        SELECT * FROM users WHERE account_number = ?
        """, (account_number,))
        return self.cursor.fetchone()

    def get_user_by_pesel(self, pesel):
        self.cursor.execute("""
        SELECT * FROM users WHERE pesel = ?
        """, (pesel,))
        return self.cursor.fetchone()

    def update_balance(self, account_number, new_balance):
        self.cursor.execute("""
        UPDATE users SET balance = ?
        WHERE account_number = ?
        """, (new_balance, account_number))
        self.conn.commit()

    def get_balance(self, account_number):
        self.cursor.execute("""
        SELECT balance FROM users WHERE account_number = ?
        """, (account_number,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.conn.close()