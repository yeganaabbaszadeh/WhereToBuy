from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from amazon import *
import csv

views = Blueprint('views', __name__)
data = []


@views.route('/', methods=["GET", "POST"])
# @login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/about")
def about():
	return render_template("about.html", title='About')

@views.route("/search/<item>")
def find(item):
    data.clear()
    scraper(item)
    with open('results.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_num = 0
        for row in csv_reader:
            if line_num != 0:
                if row['price'] != "":
                    row['price'] = row['price'] + '$'
                else:
                    row['price'] = 'Information about price is not available.'
                ls_temp = [row['title'], 'https://www.amazon.com/' + row['link'], row['price']]
                data.append(ls_temp)
            line_num = line_num + 1

    return render_template('home.html', user=current_user, isSearching = True, items=data)


# @views.route('/products', methods=['GET', 'POST'])
# def products():
#     data.clear()
#     if request.method == "POST":
#         if request.form['search_button'] == 'Search':
#             return redirect(url_for('views.find', item=request.form.get('search_text')))
#     return redirect(url_for('views.home'))