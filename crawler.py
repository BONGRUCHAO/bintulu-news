import feedparser
import requests
from bs4 import BeautifulSoup


def get_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        for t in soup(["script", "style", "noscript"]):
            t.decompose()

        ps = soup.find_all("p")
        text = " ".join(p.get_text() for p in ps)

        return text[:2000]

    except:
        return ""


def crawl_news():
    try:
        feed = feedparser.parse(
            "https://news.google.com/rss/search?q=Bintulu&hl=en-MY&gl=MY&ceid=MY:en"
        )

        if not feed or not feed.entries:
            print("RSS EMPTY")
            return []

        print("RSS ITEMS:", len(feed.entries))

        news = []

        for e in feed.entries[:10]:
            if not hasattr(e, "title") or not hasattr(e, "link"):
                continue

            news.append({
                "title": e.title,
                "link": e.link,
                "content": get_content(e.link) or e.title
            })

        return news

    except Exception as e:
        print("CRAWL FAIL:", e)
        return []
