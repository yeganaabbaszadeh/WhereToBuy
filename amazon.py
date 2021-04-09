from pathlib import Path
from selenium import webdriver
from bs4 import BeautifulSoup
import csv


DRIVER_PATH = str(Path('geckodriver').resolve())
BROWSER = webdriver.Firefox(executable_path=DRIVER_PATH)

def write_csv(ads):
    with open('results.csv', 'a+', encoding='utf-8') as f:
        fields = ['title', 'link', 'price']

        writer = csv.DictWriter(f, fieldnames=fields)

        for ad in ads:
            writer.writerow(ad)


def get_html(url):
    BROWSER.get(url)
    return BROWSER.page_source


def scrape_data(card):
    try:
        h2 = card.h2
    except:
        title = ''
        link = ''
    else:
        title = h2.text.strip()
        link = h2.a.get('href')

    try:
        price = card.find('span', class_='a-price-whole').text.strip('.').strip()
    except:
        price = ''
    else:
        price = ''.join(price.split(','))
    
    data = {'title': title, 'link': link, 'price': price}

    return data


def scraper(item):
    ads_data = []

    _f = open('results.csv', 'w+', encoding='utf-8')
    _f.write("")
    _f.close()
    _f.close()
    ads_data = []

    url = f"https://www.amazon.com/s?k={item}&page=1&qid=1617940467&ref=sr_pg_2"
    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')

    cards = soup.find_all('div', {'data-asin': True, 'data-component-type': 's-search-result'})
        
    for card in cards:
        data = scrape_data(card)
        ads_data.append(data) 

    with open('results.csv', 'a+', encoding='utf-8') as f:
        f.write("title,link,price\n")
    f.close()
    write_csv(ads_data)

