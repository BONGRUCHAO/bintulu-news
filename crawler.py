import requests
import xml.etree.ElementTree as ET

def crawl_news():
    url = "https://news.google.com/rss/search?q=Bintulu&hl=en-MY&gl=MY&ceid=MY:en"

    r = requests.get(url, timeout=10)

    root = ET.fromstring(r.content)

    news = []

    for item in root.findall(".//item"):
        title = item.find("title").text
        link = item.find("link").text

        if title and link:
            news.append({
                "title": title,
                "link": link
            })

    return news[:15]
