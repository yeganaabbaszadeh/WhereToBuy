from .scraper import *

class TapAzScraper(WebScraper):
    def __init__(self, item):
        super().__init__(item)

    def scrape_data(self, card):
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

    def get_data(self, item):
        ads_data = []
        _f = open('webscrapers/results.csv', 'a+', encoding='utf-8')
        _f.write("")
        _f.close()
        
        url = f'https://tap.az/elanlar?utf8=%E2%9C%93&log=true&keywords={item}&q%5Bregion_id%5D='
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        cards = soup.find_all('div', {'class': 'products-i rounded'})
        
        for card in cards:
            data = self.scrape_data(card)
            ads_data.append(data)
            
        with open('webscrapers/results.csv', 'a+', encoding='utf-8') as f:
            f.write("title,link,price, page\n") 
        f.close()
        self.write_csv(ads_data)
        return _f
