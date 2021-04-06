from website import create_app

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, render_template, request, redirect
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__, template_folder="website/templates")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
# db = SQLAlchemy(app)


# @app.route("/")
# def home():
#     return render_template("home.html")

# @app.route("/about")
# def about():
# 	return render_template("about.html", title='About')


# if __name__ == "__main__":
#     app.run(debug=True)
