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
        INSERT OR IGNORE INTO news
        (title, link, content, summary, category, time)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (title, link, content, summary, category))

        if c.rowcount == 0:
            print("SKIP DUPLICATE:", title[:30])
        else:
            print("INSERT OK:", title[:30])

        conn.commit()

    except Exception as e:
        print("DB ERROR:", e)

    finally:
        conn.close()

def get_news():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    SELECT title, link, summary, category, time
    FROM news
    ORDER BY id DESC
    LIMIT 100
    """)

    rows = c.fetchall()
    conn.close()
    return rows
