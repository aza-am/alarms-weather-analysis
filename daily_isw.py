from bs4 import BeautifulSoup
import requests
import time
import csv
from datetime import datetime, timedelta

#весь код ппереважно взятий з іншого -> historical_data_isw.py

BASE = "https://understandingwar.org"

headers = {"User-Agent": "Mozilla/5.0"}


today = datetime.now()
yesterday = today - timedelta(days=1)

today_str = today.strftime("%B %d, %Y").replace(" 0", " ")   #саме в такому форматі дати на сайті
yesterday_str = yesterday.strftime("%B %d, %Y").replace(" 0", " ")


file = f"war_reports_{today_str}.csv"


url = f"{BASE}/research/?_teams=russia-ukraine&_paged=1"

req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, "html.parser")

articles = soup.select("h3.research-card-title a")
links = [a["href"] for a in articles]

print(f"--> {len(links)} links on this page")



with open(file, "w", newline="", encoding="utf-8") as f:
    

    writer = csv.writer(f)
    writer.writerow(["url", "date", "text"])


    for link in links:
        print("Now looking on --> ", link)

        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")

        date_tag = soup.find("h6", class_="gb-text")
        date = date_tag.text.strip() if date_tag else ""


        if date != today_str and date != yesterday_str:
            continue

        text = ""

        toplines = soup.find("div", id="toplines")

        if toplines:
            strong = toplines.find("strong")
            if strong:
                text = strong.get_text(strip=True)

        if not text:

            content = soup.find("div", class_="entry-content")

            if content:
                paragraphs = content.find_all("p")
            else:
                paragraphs = soup.find_all("p")

            for p in paragraphs:

                strong = p.find("strong")

                if strong:
                    candidate = strong.get_text(strip=True)

                    if len(candidate) < 200:
                        continue

                    text = candidate
                    break


        writer.writerow([link, date, text])
        f.flush()
        time.sleep(1)


    print(f"--> CSV file ready and saved --> {file}")