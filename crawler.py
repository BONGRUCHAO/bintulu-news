import requests
import xml.etree.ElementTree as ET

def crawl_news():
    url = "https://news.google.com/rss/search?q=Bintulu&hl=en-MY&gl=MY&ceid=MY:en"

    r = requests.get(url, timeout=10)

    print("STATUS:", r.status_code)
    print("CONTENT SIZE:", len(r.content))

    root = ET.fromstring(r.content)
    items = root.findall(".//item")

    print("RSS ITEMS:", len(items))

    news = []

    for i in items[:5]:
        title = i.find("title").text
        link = i.find("link").text

        print("TITLE:", title)

        news.append({
            "title": title,
            "link": link
        })

    return news
