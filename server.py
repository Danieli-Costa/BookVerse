"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import requests
import os
import json


app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"
app.jinja_env.undefined = StrictUndefined


# API keys

GOOGLE_BOOKS_KEY = os.environ["GOOGLE_BOOKS_KEY"]


@app.route("/")
def homepage():
    """View homepage"""

    return render_template("homepage.html")


@app.route("/log_in")
def log_in():
    """View log in and create account"""

    return render_template("log_in.html")


@app.route("/create", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password, first_name, last_name)

        flash("Account created! Please log in.")

    return redirect("/")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")


@app.route("/lookup")
def result_search():
    """Show the results of a book search"""

    search = request.args.get("search-book")

    search_split = search.split()

    title = "+".join(search_split)

    url = f"https://www.googleapis.com/books/v1/volumes?q={title}&printType=books&projection=full&orderBy=relevance"
    payload = {"key": GOOGLE_BOOKS_KEY}
    response = requests.get(url, params=payload)

    data = response.json()

    # books_list = []

    num_results = data.get("totalItems")

    items_list = data.get("items")

    return render_template("book_results.html", items_list=items_list, num_results=num_results)


@app.route("/details/<item_id>")
def book_details(item_id):
    """Shows details of a specific book"""

    url = f"https://www.googleapis.com/books/v1/volumes/{item_id}"
    payload = {"key": GOOGLE_BOOKS_KEY}
    response = requests.get(url, params=payload)

    data = response.json()
    print('*'*20)
    details_list = data.get("volumeInfo")
    print(details_list)
    return render_template("book_details.html", details_list=details_list)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
