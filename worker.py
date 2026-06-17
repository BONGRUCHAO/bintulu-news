import time
from crawler import crawl_news
from db import init_db, insert_news
from ai import analyze

init_db()

# ====== 限流配置 ======
MAX_AI_PER_RUN = 3      # 每次最多处理3条
SLEEP_BETWEEN_AI = 5    # 每条间隔5秒


def run_job():
    print("START JOB")

    news_list = crawl_news()

    count = 0

    for n in news_list:

        if count >= MAX_AI_PER_RUN:
            print("LIMIT REACHED, STOP THIS ROUND")
            break

        category, summary = analyze(n["title"])

        insert_news(
            n["title"],
            n["link"],
            "",
            summary,
            category
        )

        count += 1

        print("AI DONE:", n["title"])

        time.sleep(SLEEP_BETWEEN_AI)


while True:
    run_job()

    print("SLEEP 30 MIN")
    time.sleep(1800)
