import sqlite3

class Database:
    def __init__(self, db_file="sentinel.db"):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repo_name TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS updates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repo_name TEXT NOT NULL,
                    event_type TEXT,
                    event_time TEXT
                )
            """)

    def add_update(self, repo_name, event_type, event_time):
        with self.conn:
            self.conn.execute("""
                INSERT INTO updates (repo_name, event_type, event_time)
                VALUES (?, ?, ?)
            """, (repo_name, event_type, event_time))
