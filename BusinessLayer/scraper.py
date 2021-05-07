from pathlib import Path
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import html
from time import sleep
import csv
import os


DRIVER_PATH = str(Path('BusinessLayer/geckodriver').resolve())
BROWSER = webdriver.Firefox(executable_path=DRIVER_PATH)


class WebScraper:
    def __init__(self, item):
        self.item = item

    def write_csv(self, ads):
        with open('BusinessLayer/results.csv', 'a+', encoding='utf-8') as f:
            fields = ['title', 'link', 'price', 'page']
            writer = csv.DictWriter(f, fieldnames=fields)

            for ad in ads:
                writer.writerow(ad)

    def get_html(self, url):
        BROWSER.get(url)
        return BROWSER.page_source

    def scrape_data(self, card):
        pass

    def get_data(self, item):
        pass

