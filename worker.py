import time
import sqlite3
from crawler import crawl_news
from db import init_db, insert_news
from ai import analyze

init_db()


def exists(link):
    conn = sqlite3.connect("news.db")
    c = conn.cursor()

    c.execute("SELECT 1 FROM news WHERE link=?", (link,))
    result = c.fetchone()

    conn.close()

    return result is not None


def run_job():
    print("START JOB")

    news_list = crawl_news()

    for n in news_list:

        # ⭐ 核心：已存在就跳过（完全避免AI重复）
        if exists(n["link"]):
            print("SKIP EXIST:", n["title"])
            continue

        category, summary = analyze(n["title"])

        insert_news(
            n["title"],
            n["link"],
            "",
            summary,
            category
        )

        print("NEW:", n["title"])


while True:
    run_job()
    print("SLEEP 30 MIN")
    time.sleep(1800)
