import requests
from bs4 import BeautifulSoup

def crawl_news():
    url = "https://news.google.com/search?q=Bintulu&hl=en-MY&gl=MY&ceid=MY:en"

    r = requests.get(url)
    print("STATUS:", r.status_code)
    print("HTML length:", len(r.text))

    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    for a in soup.find_all("a"):
        title = a.text.strip()
        href = a.get("href")

        if title:
            results.append(title)

    print("FOUND TITLES:", len(results))

    return []
