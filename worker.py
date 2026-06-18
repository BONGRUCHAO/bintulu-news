import time
from crawler import crawl_news
from db import init_db, insert_news
from ai import analyze

init_db()

MAX_PER_RUN = 5
SLEEP_BETWEEN = 3


def safe_analyze(title, content):
    try:
        return analyze(title, content)
    except Exception as e:
        print("AI FAIL:", e)
        return "其他", title[:30]


def run_job():
    print("START JOB")

    try:
        news_list = crawl_news()
    except Exception as e:
        print("CRAWL FAIL:", e)
        return

    if not news_list:
        print("NO NEWS FOUND")
        return

    count = 0

    for n in news_list:

        if count >= MAX_PER_RUN:
            break

        try:
            category, summary = safe_analyze(n["title"], n["content"])

            insert_news(
                n["title"],
                n["link"],
                n["content"],
                summary,
                category
            )

            print("DONE:", n["title"])

        except Exception as e:
            print("INSERT FAIL:", e)

        count += 1
        time.sleep(SLEEP_BETWEEN)


# ===== 永久运行 + 防崩 =====
while True:
    try:
        run_job()
    except Exception as e:
        print("WORKER CRASH PROTECTED:", e)

    print("SLEEP 30 MIN")
    time.sleep(1800)
