from flask import Flask, render_template
from db import init_db, insert_news, get_news
from crawler import crawl_news
from ai import summarize

app = Flask(__name__)

init_db()

def update_data():
    news_list = crawl_news()

    for n in news_list:
        summary = summarize(n["title"])
        insert_news(n["title"], n["link"], "", summary)

@app.route("/")
def index():
    update_data()
    news = get_news()
    return render_template("index.html", news=news)

if __name__ == "__main__":
    app.run(debug=True)
