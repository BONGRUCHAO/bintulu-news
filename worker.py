import time
from crawler import crawl_news
from db import init_db, insert_news
from ai import analyze

init_db()

MAX_PER_RUN = 5
SLEEP_BETWEEN = 3


def run_job():
    print("START JOB")

    news_list = crawl_news()

    count = 0

    for n in news_list:

        if count >= MAX_PER_RUN:
            break

        category, summary = analyze(n["title"], n["content"])

        insert_news(
            n["title"],
            n["link"],
            n["content"],
            summary,
            category
        )

        print("DONE:", n["title"])

        count += 1
        time.sleep(SLEEP_BETWEEN)


while True:
    run_job()
    print("SLEEP 30 MIN")
    time.sleep(1800)
