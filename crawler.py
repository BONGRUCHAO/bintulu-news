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

        return text[:2500]

    except:
        return ""


def crawl_news():
    feed = feedparser.parse(
        "https://www.theborneopost.com/feed/"
    )

    print("RSS ITEMS:", len(feed.entries))

    news = []

    for e in feed.entries[:10]:

        # ⭐ 获取发布时间（关键）
        published = getattr(e, "published", None)

        news.append({
            "title": e.title,
            "link": e.link,
            "content": get_content(e.link),
            "published": published  # ⭐ 新增
        })

    return news
