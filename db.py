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
        category TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_news(title, link, content, summary, category):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute("""
        INSERT INTO news (title, link, content, summary, category, time)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (title, link, content, summary, category))

        conn.commit()

    except sqlite3.IntegrityError:
        # 已存在（重复新闻）
        print("SKIP DUPLICATE:", title)

    conn.close()
