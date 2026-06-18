import sqlite3

DB_NAME = "news.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        link TEXT UNIQUE,
        content TEXT,
        summary TEXT,
        category TEXT,
        published_time TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_news(title, link, content, summary, category, published_time):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute("""
        INSERT INTO news (
            title, link, content, summary, category, published_time, time
        )
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """, (title, link, content, summary, category, published_time))

        conn.commit()

    except sqlite3.IntegrityError:
        print("DUPLICATE:", title)

    conn.close()


def get_news():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    SELECT title, link, summary, category, published_time, time
    FROM news
    ORDER BY id DESC
    """)

    rows = c.fetchall()
    conn.close()
    return rows
