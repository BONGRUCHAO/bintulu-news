import time
from crawler import crawl_news
from db import init_db, insert_news
from ai import analyze

init_db()

def run_job():
    print("START JOB")

    news_list = crawl_news()

    for n in news_list:
        category, summary = analyze(n["title"])

        insert_news(
            n["title"],
            n["link"],
            "",
            summary,
            category
        )

        print("DONE:", n["title"])


# 无限循环后台运行
while True:
    run_job()

    print("SLEEP 30 MIN")
    time.sleep(1800)
