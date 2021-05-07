from .scraper import *

class AmazonScraper(WebScraper):
    def __init__(self, item):
        super().__init__(item)

    def scrape_data(self, card):
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

    def get_data(self, item):
        ads_data = []
        _f = open('BusinessLayer/results.csv', 'w+', encoding='utf-8')
        _f.write("")
        _f.close()
        os.remove('BusinessLayer/results.csv')
        _f = open('BusinessLayer/results.csv', 'x', encoding='utf-8')
        _f.close()
        ads_data = []

        for i in range(1, 10):
            url = f"https://www.amazon.com/s?k={item}&page={i}&qid=1617940467&ref=sr_pg_2"
            html = self.get_html(url)
            soup = BeautifulSoup(html, 'lxml')
            cards = soup.find_all('div', {'data-asin': True, 'data-component-type': 's-search-result'})
                
            for card in cards:
                data = self.scrape_data(card)
                ads_data.append(data) 

        with open('BusinessLayer/results.csv', 'a+', encoding='utf-8') as f:
            f.write("title,link,price,page\n")
        f.close()
        self.write_csv(ads_data)
        return _f