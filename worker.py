import time
from crawler import crawl_news
from db import init_db, insert_news
from ai import analyze

init_db()

def run_job():
    print("START JOB")

    news_list = crawl_news()

    print("TOTAL RSS:", len(news_list))

    for n in news_list:

        # 直接插入（靠DB去重）
        category, summary = analyze(n["title"])

        insert_news(
            n["title"],
            n["link"],
            "",
            summary,
            category
        )

        print("PROCESSED:", n["title"])


while True:
    run_job()

    print("SLEEP 30 MIN")
    time.sleep(1800)
