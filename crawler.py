import feedparser
import requests
from bs4 import BeautifulSoup


def get_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, headers=headers, timeout=6)

        if r.status_code != 200:
            return ""

        soup = BeautifulSoup(r.text, "html.parser")

        for t in soup(["script", "style", "noscript"]):
            t.decompose()

        ps = soup.find_all("p")
        text = " ".join(p.get_text() for p in ps)

        text = text.strip()

        return text[:1500] if text else ""

    except Exception as e:
        print("CONTENT FAIL:", e)
        return ""


def crawl_news():
    try:
        url = "https://news.google.com/rss/search?q=Bintulu&hl=en-MY&gl=MY&ceid=MY:en"

        feed = feedparser.parse(url)

        # 🔥关键检查1
        if not feed:
            print("FEED NONE")
            return []

        # 🔥关键检查2
        if hasattr(feed, "status"):
            print("RSS STATUS:", feed.status)

        # 🔥关键检查3
        if not feed.entries:
            print("RSS EMPTY (blocked or failed parsing)")
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
