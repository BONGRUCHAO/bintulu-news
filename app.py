from flask import Flask, render_template
from crawler import crawl_news
from db import init_db, insert_news, get_news

print("ROUTE HIT")
app = Flask(__name__)
init_db()

@app.route("/")
def index():

    news_list = crawl_news()

    print("CRAWLED:", len(news_list))

    for n in news_list:
        insert_news(n["title"], n["link"], "", "")

    news = get_news()

    return render_template("index.html", news=news)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
