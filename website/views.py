from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from webscrapers.amazon import *
import csv

views = Blueprint('views', __name__)
data = []
ls_temp = []


@views.route('/', methods=["GET", "POST"])
def home():
    return render_template("home.html", user=current_user)


@views.route('/about')
def about():
	return render_template("about.html", title='About')


@views.route('/search/', methods=['GET', 'POST'])
def search_items():
    item = request.form['search_item']
    data.clear()
    amazonScraper(item)
    with open('webscrapers/results.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_num = 0
        for row in csv_reader:
            if line_num != 0:
                if row['price'] != "":
                    row['price'] =  '$' + row['price']
                else:
                    row['price'] = "Pricing information not available." 
                ls_temp = [row['title'], 'https://www.amazon.com/' + row['link'], row['price']]
                data.append(ls_temp)
            line_num = line_num + 1

    return render_template('home.html', user=current_user, isSearching = True, items=data, item=request.form.get('search_item'))
