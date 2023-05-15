"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import requests
import os


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


# @app.route("/results-search")
# def result_search():
#     """Show the results of a book search"""

#     title = request.form.get("search-book")

#     url = "https://www.googleapis.com/books/v1/volumes?q=search+terms"
#     payload = {"apikey": GOOGLE_BOOKS_KEY}
#      =

#     return render_template("book-results.html")


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
