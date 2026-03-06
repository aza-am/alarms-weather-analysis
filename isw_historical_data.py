from bs4 import BeautifulSoup
import requests
import time
import csv
from datetime import datetime

BASE = "https://understandingwar.org"

headers = {
    "User-Agent": "Mozilla/5.0"
    # для "безпечного скрапінгу' сайту, щоб не заблокували
}

START_DATE = datetime(2022, 2, 24)
END_DATE = datetime(2026, 3, 1)

#--------------------1)Збирання лінків з сайту----------------------------------------------------------

links = []

for page in range(1, 59):
    #найперша потрібна дата знаходиться на 58й сторінці, так як збір відбувається 1 раз, то можна брати саме таку кількість сторінок, 
    # АЛЕ якщо  запускати цей код в інші дні то треба перевіряти на якій сторінці подія з датою 24.02.2022 щоб взяти всі події з потрібного інтервалу
    #за логікою можна брати і всі сторінки що є, але нащо зайвий раз перевіряти купу непотрібних лінків, якщо дані збираються 1 раз

    url = f"{BASE}/research/?_teams=russia-ukraine&_paged={page}"
    print("Scanning page --> ", page)

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")

    articles = soup.select("h3.research-card-title a")
                            #усі потрібні силки на події загорнуті саме в цей заголовок / клас
    if not articles:
        break

    for a in articles:
        links.append(a["href"])

    time.sleep(0.5)
          #щоб запити приходили через якийсь проміжок часу, а не всі одразу

print("Total links:", len(links))


#-------------------------2)Збирання інформації з кожного лінка-------------------------------------------------------

#data = []


with open("isw_historical_data.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)
    writer.writerow(["url", "date", "text"])


    for link in links:

        print("Now looking on --> ", link)

        req = requests.get(link, headers=headers)
        if req.status_code != 200:
            print("Failed:", link)
            continue

        soup = BeautifulSoup(req.text, "html.parser")

        date_tag = soup.find("h6", class_="gb-text")
        date = date_tag.text.strip() if date_tag else ""

        try:
            date_obj = datetime.strptime(date, "%B %d, %Y")
        except:
            continue

        if not (START_DATE <= date_obj <= END_DATE):
            continue

        # toplines = soup.find("div", id="toplines")
        # text = ""
        # if toplines:
        #     first = toplines.find("strong")
        #     if first:
        #         text = first.get_text(strip=True)  --> не всюди є топлайн тому не завжди працює

        # text = ""

        # first_strong = soup.find("strong")
        # if first_strong:
        #     text = first_strong.get_text(strip=True) --> іноді перший p це і є тайтл + дата, а нам це не треба


        text = ""

        def is_valid_paragraph(candidate, min_len=80):
            skip_words = ["Click here", "map", "ISW", "interactive", "archive", "Note"]
            
            if len(candidate) < min_len:
                return False
            if "." not in candidate:
                return False
            for word in skip_words:
                if word in candidate:
                    return False
            return True

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
                candidate = strong.get_text(strip=True) if strong else p.get_text(strip=True)
                if is_valid_paragraph(candidate, 200):
                    text = candidate
                    break

            if not text:
                for p in paragraphs:
                    strong = p.find("strong")
                    candidate = strong.get_text(strip=True) if strong else p.get_text(strip=True)
                    if is_valid_paragraph(candidate, 80):
                        text = candidate
                        break



        writer.writerow([link, date, text])

        f.flush()

        print("--> Saved")

        time.sleep(0.01)

# with open("war_reports.csv", "w", newline="", encoding="utf-8") as f:

#     fieldnames = ["url", "date", "text"]

#     writer = csv.DictWriter(f, fieldnames=fieldnames)

#     writer.writeheader()
#     writer.writerows(data)  --> погана всерія, 
#                              бо краще записувати дані одразу в файл як тільки ми відкриваємо лінк, а не після проходження всіх лінків

print("--> CSV file ready and saved")