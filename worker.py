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

    try:
        category, summary = analyze(n["title"], n["content"])
    except Exception as e:
        print("ANALYZE CRASH:", e)
        category = "其他"
        summary = n["title"][:30]

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
    try:
        run_job()
    except Exception as e:
        print("WORKER ERROR:", e)

    time.sleep(1800)
