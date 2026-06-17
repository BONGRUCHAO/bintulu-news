import requests
from bs4 import BeautifulSoup
import feedparser


def get_article_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # 去掉script/style
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        # 尽量抓正文
        paragraphs = soup.find_all("p")
        content = " ".join([p.get_text() for p in paragraphs])

        return content[:3000]  # 限制长度，防止token爆

    except:
        return ""


def crawl_news():
    feed = feedparser.parse("https://www.thestar.com.my/rss")

    news_list = []

    for entry in feed.entries[:10]:

        content = get_article_content(entry.link)

        news_list.append({
            "title": entry.title,
            "link": entry.link,
            "content": content
        })

    return news_list
