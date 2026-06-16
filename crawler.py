import requests
from bs4 import BeautifulSoup

def crawl_news():
    url = "https://news.google.com/search?q=Bintulu&hl=en-MY&gl=MY&ceid=MY:en"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    for a in soup.find_all("a"):
        title = a.text.strip()
        href = a.get("href")

        if title and href and "/articles/" in href:
            link = "https://news.google.com" + href[1:]

            results.append({
                "title": title,
                "link": link
            })

    return results[:10]
