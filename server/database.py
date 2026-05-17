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
            name TEXT,
            surname TEXT,
            pesel TEXT UNIQUE,
            account_number TEXT UNIQUE,
            password_hash TEXT,
            balance REAL DEFAULT 0
        )
        """)
        self.conn.commit()

    def create_user(self, name, surname, pesel, acc, pwd_hash):
        try:
            self.cursor.execute("""
            INSERT INTO users (name, surname, pesel, account_number, password_hash, balance)
            VALUES (?, ?, ?, ?, ?, 0)
            """, (name, surname, pesel, acc, pwd_hash))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user_by_account(self, acc):
        self.cursor.execute("SELECT * FROM users WHERE account_number = ?", (acc,))
        return self.cursor.fetchone()

    def get_balance(self, acc):
        self.cursor.execute("SELECT balance FROM users WHERE account_number = ?", (acc,))
        res = self.cursor.fetchone()
        return res[0] if res else None

    def transfer(self, from_acc, to_acc, amount):
        self.cursor.execute("SELECT balance FROM users WHERE account_number = ?", (from_acc,))
        sender = self.cursor.fetchone()

        self.cursor.execute("SELECT balance FROM users WHERE account_number = ?", (to_acc,))
        receiver = self.cursor.fetchone()

        if not sender or not receiver:
            return "ERROR: ACCOUNT NOT FOUND"

        if sender[0] < amount:
            return "ERROR: NOT ENOUGH MONEY"

        self.cursor.execute("UPDATE users SET balance = ? WHERE account_number = ?",
                            (sender[0] - amount, from_acc))

        self.cursor.execute("UPDATE users SET balance = ? WHERE account_number = ?",
                            (receiver[0] + amount, to_acc))

        self.conn.commit()
        return "TRANSFER SUCCESS"

    def deposit(self, acc, amount):
        self.cursor.execute("SELECT balance FROM users WHERE account_number = ?", (acc,))
        user = self.cursor.fetchone()

        if not user:
            return "ERROR: ACCOUNT NOT FOUND"

        new_balance = user[0] + amount

        self.cursor.execute("UPDATE users SET balance = ? WHERE account_number = ?",
                            (new_balance, acc))
        self.conn.commit()

        return "DEPOSIT SUCCESS"

    def withdraw(self, acc, amount):
        self.cursor.execute("SELECT balance FROM users WHERE account_number = ?", (acc,))
        user = self.cursor.fetchone()

        if not user:
            return "ERROR: ACCOUNT NOT FOUND"

        if user[0] < amount:
            return "ERROR: NOT ENOUGH MONEY"

        new_balance = user[0] - amount

        self.cursor.execute("UPDATE users SET balance = ? WHERE account_number = ?",
                            (new_balance, acc))
        self.conn.commit()

        return "WITHDRAW SUCCESS"