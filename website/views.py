from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from webscrapers.scraper import *
import csv

views = Blueprint('views', __name__)
amazon_data = []
tapaz_data = []
# aliexpress_data = []


@views.route('/', methods=["GET", "POST"])
def home():
    return render_template("home.html", user=current_user)


@views.route('/about')
def about():
	return render_template("about.html", title='About', user=current_user)


@views.route('/search', methods=['GET', 'POST'])
def search():
    item = request.form['search_item']
    amazon_data.clear()
    tapaz_data.clear()
    amazonScraper(item)
    tapazScraper(item)
    # aliexpressScraper(item)

    if request.method == "POST":
        sites = request.form.getlist('site')
        min_price = int(request.form.get('from')) if request.form.get('from') != '' else 0
        max_price = int(request.form.get('to')) if request.form.get('to') != '' else 10000
        currency = request.form.get('currency')
        order = request.form.get('order')

    # print(f"{min_price}, {max_price}")
    # print(currency)
    # print(order)


    with open('webscrapers/results.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_num = 0
        for row in csv_reader:
            if line_num != 0:
                if row['page'] == 'amazon':
                    if row['price'] != "":
                        if min_price < int(row['price']) < max_price:
                            if currency == 'usd':
                                row['price'] = '$' + row['price']
                            else:
                                row['price'] = str(float(row['price']) * 1.70) + ' AZN'

                            amazon_ls = [row['title'], 'https://www.amazon.com/' + row['link'], row['price'], row['page']]
                        else:
                            continue
                    else:
                        continue

                    amazon_data.append(amazon_ls)

                elif row['page'] == 'tapaz':
                    if row['price'] != "":
                        if min_price < int(row['price']) < max_price:
                            if currency == 'usd':
                                row['price'] = '$' + str(float(row['price']) / 1.70)
                            else:
                                row['price'] = row['price'] + ' AZN'

                            tapaz_ls = [row['title'], 'https://tap.az' + row['link'], row['price'], row['page']]
                        else:
                            continue
                    else:
                        continue
                            
                    tapaz_data.append(tapaz_ls)

                # elif row['page'] == 'aliexpress':
                #     if row['price'] != "":
                #         if min_price < int(row['price']) < max_price:
                #             aliexpress_ls = [row['title'], 'https:' + row['link'], row['price'], row['page']]
                #         else:
                #             continue
                #     else:
                #         row['price'] = "Pricing information not available."
                #         aliexpress_ls = [row['title'], 'https:' + row['link'], row['price'], row['page']]

                    
                #     aliexpress_data.append(aliexpress_ls)


            line_num = line_num + 1

    return render_template('home.html', user=current_user, isSearching = True, amazonItems=amazon_data, tapazItems=tapaz_data, item=request.form.get('search_item'), sites=request.form.getlist('site'), min_price=min_price, max_price=max_price, currency=currency, order = request.form.get('order'))


