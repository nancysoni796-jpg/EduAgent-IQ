import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("data.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            question TEXT,
            answer TEXT
        )
        """)
        self.conn.commit()

    def add_user(self, username, password):
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?,?)",
                (username, password)
            )
            self.conn.commit()
            return True
        except:
            return False

    def login_user(self, username, password):
        self.cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        return self.cursor.fetchone()

    def save_chat(self, username, q, a):
        self.cursor.execute(
            "INSERT INTO chats (username, question, answer) VALUES (?,?,?)",
            (username, q, a)
        )
        self.conn.commit()

    def get_chats(self, username):
        self.cursor.execute(
            "SELECT question, answer FROM chats WHERE username=? ORDER BY id DESC LIMIT 10",
            (username,)
        )
        return self.cursor.fetchall()