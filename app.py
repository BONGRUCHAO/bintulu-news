from flask import Flask, render_template
from crawler import crawl_news
from db import init_db, insert_news, get_news

app = Flask(__name__)
init_db()

# 是否已经初始化过数据（避免每次访问都爬）
DATA_READY = False


def load_data_once():
    global DATA_READY

    if DATA_READY:
        return

    print("FIRST TIME LOADING NEWS...")

    news_list = crawl_news()

    print("CRAWLED:", len(news_list))

    for n in news_list:
        insert_news(n["title"], n["link"], "", "")

    DATA_READY = True


@app.route("/")
def index():

    load_data_once()

    news = get_news()

    print("NEWS COUNT:", len(news))

    return render_template("index.html", news=news)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)