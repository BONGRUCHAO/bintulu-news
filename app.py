from flask import Flask, render_template
from db import init_db, get_news
from crawler import crawl_news
from ai import analyze, safe_analyze
from db import insert_news
import time

app = Flask(__name__)
init_db()

# 防止频繁爬取（关键）
last_update = 0
UPDATE_INTERVAL = 300  # 5分钟


def update_news_if_needed():
    global last_update

    now = time.time()

    # 5分钟内不重复更新
    if now - last_update < UPDATE_INTERVAL:
        return

    print("AUTO UPDATE START")

    try:
        news_list = crawl_news()

        if not news_list:
            print("EMPTY RSS")
            return

        for n in news_list[:5]:  # 控制负载
            category, summary = safe_analyze(n["title"], n["content"])

            insert_news(
                n["title"],
                n["link"],
                n["content"],
                summary,
                category
            )

        last_update = now
        print("AUTO UPDATE DONE")

    except Exception as e:
        print("UPDATE FAIL:", e)


@app.route("/")
def index():
    t1 = time.time()

    update_news_if_needed()

    t2 = time.time()
    print("UPDATE TIME:", t2 - t1)

    news = get_news() or []

    return render_template("index.html", news=news)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
