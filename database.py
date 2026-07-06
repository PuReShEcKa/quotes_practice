import sqlite3


class QuotesDB:
    def __init__(self):
        self.conn = sqlite3.connect('quotes.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS quotes(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                text TEXT NOT NULL,
                                author TEXT,
                                category TEXT,
                                date TEXT,
                                is_favorite INTEGER DEFAULT 0,
                                image_path TEXT
                            )
                            ''')
        self.conn.commit()

    def add_quote(self, text, author, category, date, is_favorite, image_path):
        self.cursor.execute('''
                            INSERT INTO quotes (text, author, category, date, is_favorite, image_path)
                            VALUES (?, ?, ?, ?, ?, ?)
                            ''', (text, author, category, date, is_favorite, image_path))
        self.conn.commit()

    def get_all_quotes(self):
        self.cursor.execute('SELECT * FROM quotes ORDER BY date DESC')
        return self.cursor.fetchall()

    def delete_quote(self, quote_id):
        self.cursor.execute('DELETE FROM quotes WHERE id = ?', (quote_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()