import sqlite3

DB_NAME = "news.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        link TEXT,
        content TEXT,
        summary TEXT,
        time TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_news(title, link, content, summary):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
    INSERT INTO news (title, link, content, summary, time)
    VALUES (?, ?, ?, ?, datetime('now'))
    """, (title, link, content, summary))
    conn.commit()
    conn.close()

def get_news():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT title, link, summary, time FROM news ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows
