from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from webscrapers.scraper import *
import csv

views = Blueprint('views', __name__)
amazon_data = []
amazon_ls = []
tapaz_data = []
tapaz_ls = []
aliexpress_data = []
aliexpress_ls = []


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
    aliexpressScraper(item)

    if request.method == "POST":
        sites = request.form.getlist('site')

    print(sites)

    with open('webscrapers/results.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_num = 0
        for row in csv_reader:
            if line_num != 0:
                if row['page'] == 'amazon':
                    if row['price'] != "":
                        row['price'] =  '$' + row['price']
                    else:
                        row['price'] = "Pricing information not available." 
                                
                    amazon_ls = [row['title'], 'https://www.amazon.com/' + row['link'], row['price'], row['page']]
                    amazon_data.append(amazon_ls)

                elif row['page'] == 'tapaz':
                    if row['price'] != "":
                        row['price'] = row['price'] + 'AZN'
                    else:
                        row['price'] = "Pricing information not available." 
                            
                    tapaz_ls = [row['title'], 'https://tap.az' + row['link'], row['price'], row['page']]
                    tapaz_data.append(tapaz_ls)

                elif row['page'] == 'aliexpress':
                    if row['price'] != "":
                        row['price'] = row['price']
                    else:
                        row['price'] = "Pricing information not available." 

                    if row['title'] != []:
                        aliexpress_ls = [row['title'], 'https:' + row['link'], row['price'], row['page']]
                        aliexpress_data.append(aliexpress_ls)

            line_num = line_num + 1

    return render_template('home.html', user=current_user, isSearching = True, amazonItems=amazon_data, tapazItems=tapaz_data, aliexpressItems=aliexpress_data, item=request.form.get('search_item'), sites=request.form.getlist('site'))
