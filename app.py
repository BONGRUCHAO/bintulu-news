from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_news():
    url = "https://news.google.com/search?q=Bintulu&hl=en-MY&gl=MY&ceid=MY:en"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    news = []
    for a in soup.find_all("a"):
        title = a.text.strip()
        href = a.get("href")

        if title and href and "/articles/" in href:
            link = "https://news.google.com" + href[1:]
            news.append({"title": title, "link": link})

    return news[:20]

@app.route("/")
def index():
    news = get_news()
    return render_template("index.html", news=news)

if __name__ == "__main__":
    app.run()
