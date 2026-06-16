from crawler import crawl_news
from db import init_db, insert_news
from ai import summarize
import time

init_db()

def run_job():
    news_list = crawl_news()

    for n in news_list:
        summary = summarize(n["title"])
        insert_news(n["title"], n["link"], "", summary)

if __name__ == "__main__":
    while True:
        print("Updating news...")
        run_job()
        time.sleep(1800)  # 30分钟
