from pathlib import Path
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import html
from time import sleep
import csv
import os

DRIVER_PATH = str(Path('webscrapers/geckodriver').resolve())
BROWSER = webdriver.Firefox(executable_path=DRIVER_PATH)

def write_csv(ads):
    with open('webscrapers/results.csv', 'a+', encoding='utf-8') as f:
        fields = ['title', 'link', 'price', 'page']

        writer = csv.DictWriter(f, fieldnames=fields)

        for ad in ads:
            writer.writerow(ad)


def get_html(url):
    BROWSER.get(url)
    return BROWSER.page_source


def scrape_amazon_data(card):
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

    page = 'amazon'

    data = {'title': title, 'link': link, 'price': price, 'page': page}

    return data


def amazonScraper(item):
    ads_data = []

    _f = open('webscrapers/results.csv', 'w+', encoding='utf-8')
    _f.write("")
    _f.close()
    os.remove('webscrapers/results.csv')
    _f = open('webscrapers/results.csv', 'x', encoding='utf-8')
    _f.close()
    ads_data = []

    for i in range(1, 2):
        url = f"https://www.amazon.com/s?k={item}&page={i}&qid=1617940467&ref=sr_pg_2"
        html = get_html(url)

        soup = BeautifulSoup(html, 'lxml')

        cards = soup.find_all('div', {'data-asin': True, 'data-component-type': 's-search-result'})
            
        for card in cards:
            data = scrape_amazon_data(card)
            ads_data.append(data) 

    with open('webscrapers/results.csv', 'a+', encoding='utf-8') as f:
        f.write("title,link,price,page\n")
    f.close()
    write_csv(ads_data)


def scrape_tapaz_data(card):
    title = card.find('div', class_='products-top').img.get('alt')
    link = card.find('a', class_='products-link').get('href')
    price = card.find('div', class_='products-price-container')
    page = 'tapaz'

    if price is None:
        print('')
    else:
        Price = price.div.span.text.replace(' ', '')
        
        Price = ''.join(Price.split(','))
        
        data = {'title': title, 'link': link, 'price': Price, 'page': page}
        
        return data


def tapazScraper(item):
    
    ads_data = []
    
    _f = open('webscrapers/results.csv', 'a+', encoding='utf-8')
    _f.write("")
    _f.close()
    
    url = f'https://tap.az/elanlar?utf8=%E2%9C%93&log=true&keywords={item}&q%5Bregion_id%5D='
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    cards = soup.find_all('div', {'class': 'products-i rounded'})
    
    for card in cards:
        data = scrape_tapaz_data(card)
        ads_data.append(data)
        
    with open('webscrapers/results.csv', 'a+', encoding='utf-8') as f:
        f.write("title,link,price, page\n")
        
    f.close()
    write_csv(ads_data)


def scrape_aliexpress_data(item):

    search_data = []

    for page_num in range(1, 2):
        BROWSER.get(f'https://www.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText={item}&ltype=wholesale&SortType=default&page={page_num}')
        sleep(1)

        tree = html.fromstring(BROWSER.page_source)

        BROWSER.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(1)

        for product_tree in tree.xpath('//li[@class="list-item"]'):
            title = product_tree.xpath('.//a[@class="item-title"]/@title')
            link = product_tree.xpath('.//a[@class="store-name"]/@href')
            price = product_tree.xpath('.//span[@class="price-current"]/text()')
            # review = product_tree.xpath('.//span[@class="rating-value"]/text()')
            page = 'aliexpress'

            if price is None:
                print('')
            else:
                Price = price.span.text.replace(' ', '')
            
            Price = ''.join(Price.split(','))

            if title != []:
                data = {'title': title[0], 'link': link[0], 'price': price[0], 'page': page}
                search_data.append(data)
        return search_data
        

def aliexpressScraper(item):
    
    ads_data = []
    
    _f = open('webscrapers/results.csv', 'a+', encoding='utf-8')
    _f.write("")
    _f.close()
    
    ads_data = scrape_aliexpress_data(item)
        
    with open('webscrapers/results.csv', 'a+', encoding='utf-8') as f:
        f.write("title,link,price, page\n")
        
    f.close()
    write_csv(ads_data)

