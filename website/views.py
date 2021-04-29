from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from webscrapers.scraper import *
import csv

views = Blueprint('views', __name__)
amazon_data = []
tapaz_data = []


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

    if request.method == "POST":
        sites = request.form.getlist('site')
        min_price = float(request.form.get('from')) if request.form.get('from') != '' else 0.00
        max_price = float(request.form.get('to')) if request.form.get('to') != '' else 10000.00
        currency = request.form.get('currency')
        order = request.form.get('order')
        shipping = request.form.get('shipping')

    print(order)

    with open('webscrapers/results.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_num = 0
        for row in csv_reader:
            if line_num != 0:
                if row['page'] == 'amazon':
                    if row['price'] != "":
                        shipping_option = "available"
                        if currency == 'azn':
                            row['price'] = round(float(row['price']) * 1.70, 2)
                        else:
                            row['price'] = round(float(row['price']), 2)


                        if min_price < row['price'] < max_price:
                            if currency == 'azn':
                                row['price'] = str(row['price']) + ' AZN'   
                            else:
                                row['price'] = '$' + str(row['price'])

                            amazon_ls = [row['title'], 'https://www.amazon.com/' + row['link'], row['price'], row['page'], shipping_option]
                        else:
                            continue
                    else:
                        shipping_option = "not available"
                        row['price'] = "Pricing information not available"
                        amazon_ls = [row['title'], 'https://www.amazon.com/' + row['link'], row['price'], row['page'], shipping_option]

                    if shipping == "available":
                        if amazon_ls[4] == "available":
                            amazon_data.append(amazon_ls)
                        else:
                            continue
                    else:
                        amazon_data.append(amazon_ls)

                elif row['page'] == 'tapaz':
                    if row['price'] != "":
                        shipping_option = "available"
                        if currency == 'usd':
                            row['price'] = round(float(row['price']) / 1.70, 2)
                        else:
                            row['price'] = round(float(row['price']), 2)


                        if min_price < row['price'] < max_price:
                            if currency == 'usd':
                                row['price'] = '$' + str(row['price'])
                            else:
                                row['price'] = str(row['price']) + ' AZN'

                            tapaz_ls = [row['title'], 'https://tap.az' + row['link'], row['price'], row['page'], shipping_option]
                        else:
                            continue
                    else:
                        shipping_option = "not available"
                        row['price'] = "Pricing information not available"
                        amazon_ls = [row['title'], 'https://www.amazon.com/' + row['link'], row['price'], row['page'], shipping_option]


                    if shipping == "available":
                        if tapaz_ls[4] == "available":
                            tapaz_data.append(tapaz_ls)
                        else:
                            continue
                    else:
                        tapaz_data.append(tapaz_ls)     
                    # tapaz_data.append(tapaz_ls)


            line_num = line_num + 1

    return render_template('home.html', user=current_user, isSearching = True, amazonItems=amazon_data, tapazItems=tapaz_data, item=request.form.get('search_item'), sites=sites, min_price=min_price, max_price=max_price, currency=currency, order = request.form.get('order'))


