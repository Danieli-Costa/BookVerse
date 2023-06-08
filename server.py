"""Server for book app."""

from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, db, User
import crud
from jinja2 import StrictUndefined
import requests
import os
import json
from passlib.hash import pbkdf2_sha256




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
    """View log in page"""

    return render_template("log_in.html")

@app.route("/create_account")
def create_account():
    """View create account page"""

    return render_template("create_account.html")
    

@app.route("/create", methods=["POST"])
def register_user():
    """Create a new user and bookshelf"""

    email = request.form.get("email")
    password = request.form.get("password")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    username = request.form.get("username")

    # Hash password
    hashed_password = pbkdf2_sha256.hash(password)

    user = crud.get_user_by_username(username)
    user_by_email = crud.get_user_by_email(email)

    if user or user_by_email:
        flash("Email or username already exist. Please try again or log in in your account.")
        return redirect("/log_in")
    else:
        user = crud.create_user(email, hashed_password, first_name, last_name, username)
      
        bookshelf = crud.create_bookshelf(user)

        session["user"] = username 
        session["user_id"] = user.user_id

        

    return redirect("/")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    username = request.form.get("username")
    password = request.form.get("password")

    user = crud.get_user_by_username(username)


    if user and user.username == username and pbkdf2_sha256.verify(password, user.password):
        session["user"] = username 
        session["user_id"] = user.user_id
        flash("Login successful!")
        return redirect ("/")
    else:
        flash("Usarname or password incorrect. Please try again.")
        return redirect("/log_in")

@app.route('/logout')
def logout():
    """Log out user"""

    if "user" in session:
        del session["user"]
        del session["user_id"]
        flash("Logged out! See you another time.")
    else:
        flash("You need to be logged in.")

    return redirect("/")
  


@app.route("/lookup")
def result_search():
    """Show the results of a book search"""

    search = request.args.get("search-book")

    search_split = search.split()

    title = "+".join(search_split)

    url = f"https://www.googleapis.com/books/v1/volumes?q={title}&printType=books&projection=full&langRestrict=en&maxResults=30"
    payload = {"key": GOOGLE_BOOKS_KEY}
    response = requests.get(url, params=payload)

    data = response.json()

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

    details_list = data.get("volumeInfo")
    selling_info_list = data.get("saleInfo")

    book = crud.get_book_by_api_id(item_id)
    
    if book == None:
        return render_template("book_details.html", details_list=details_list, selling_info_list=selling_info_list, item_id=item_id, reviews=[])
    else:  
        reviews = crud.get_reviews_by_api_id(item_id)
    
        return render_template("book_details.html", details_list=details_list, selling_info_list=selling_info_list, item_id=item_id, reviews=reviews)


@app.route("/bookshelf")
def show_bookshelf():
    """View user's bookshelf"""

    if "user" in session:
        
        bookshelf = crud.get_bookshelf_by_user_id(session.get("user_id"))
            
        return render_template("bookshelf.html", bookshelf=bookshelf)
    
    else:        
        return redirect ("/log_in")

@app.route("/add_to_bookshelf", methods=["POST"])
def add_bookshelf():
    """Add book to user's bookshelf"""
    
    if "user" in session:
        user_id = session.get('user_id')

        book_details_dict = {}

        book_details_dict["book_id_api"] = request.form.get("book_id_api")
        book_details_dict["title"] = request.form.get("title")
        book_details_dict["subtitle"] = request.form.get("subtitle")
        book_details_dict["authors"] = request.form.get("authors")
        book_details_dict["publisher"] = request.form.get("publisher")
        book_details_dict["published_date"] = request.form.get("published_date")
        book_details_dict["page_count"] = request.form.get("page_count")
        book_details_dict["language"] = request.form.get("language")
        book_details_dict["average_rating"] = request.form.get("average_rating")
        book_details_dict["categories"] = request.form.get("categories")
        book_details_dict["thumbnail"] = request.form.get("thumbnail")

        book_id_api = request.form.get("book_id_api")

        book_want_to_read = crud.get_book_by_api_id(book_id_api)

        if book_want_to_read == None:
            book = crud.create_book(book_id_api=book_details_dict["book_id_api"], title=book_details_dict["title"], subtitle=book_details_dict["subtitle"],
                                    authors=book_details_dict["authors"], publisher=book_details_dict["publisher"], published_date=book_details_dict["published_date"],
                                    page_count=book_details_dict["page_count"],language=book_details_dict["language"], average_rating=book_details_dict["average_rating"],
                                    categories=book_details_dict["categories"], thumbnail=book_details_dict["thumbnail"])
        else:
            book = book_want_to_read

        bookshelf = crud.get_bookshelf_by_user_id(user_id)

        
        for want_to_read in bookshelf.books:
            if want_to_read.book_id_api == book.book_id_api:
                flash("This book is already in your bookshelf.")
                return redirect("/bookshelf")
    
        
                                    
        add_book_in_bookshelf = crud.add_books_in_bookshelf(user_id, book.book_id)
        db.session.add(add_book_in_bookshelf)
        db.session.commit()
        flash("Book added to your bookshelf")           
        return redirect("/bookshelf")
    


   
@app.route("/delete_book/<book_id>")
def delete_book_from_bookshelf(book_id):
    """Remover a book from the bookshelf list"""
    
    if "user" in session:        
        bookshelf = crud.get_bookshelf_by_user_id(session["user_id"])
        book = crud.get_book_by_id(book_id)

        crud.delete_book_from_bookshelf(bookshelf, book)

        return "success"
    else:
        return "failure"
    

@app.route("/about")
def about_app():
    """Page to explain the app and it's functionalities"""

    return render_template("about_app.html")


@app.route("/write_review", methods=["POST"])
def write_review():
    """Shows the review form to the user and handles the submit of the review"""

    if "user" in session:
                        
        
        book_details_dict = {}

        book_details_dict["book_id_api"] = request.form.get("book_id_api")
        book_details_dict["title"] = request.form.get("title")
        book_details_dict["subtitle"] = request.form.get("subtitle")
        book_details_dict["authors"] = request.form.get("authors")
        book_details_dict["publisher"] = request.form.get("publisher")
        book_details_dict["published_date"] = request.form.get("published_date")
        book_details_dict["page_count"] = request.form.get("page_count")
        book_details_dict["language"] = request.form.get("language")
        book_details_dict["average_rating"] = request.form.get("average_rating")
        book_details_dict["categories"] = request.form.get("categories")
        book_details_dict["thumbnail"] = request.form.get("thumbnail")

        book_id_api = request.form.get("book_id_api")

        book_to_review = crud.get_book_by_api_id(book_id_api)

        if book_to_review == None:
            book = crud.create_book(book_id_api=book_details_dict["book_id_api"], title=book_details_dict["title"], subtitle=book_details_dict["subtitle"],
                                    authors=book_details_dict["authors"], publisher=book_details_dict["publisher"], published_date=book_details_dict["published_date"],
                                    page_count=book_details_dict["page_count"],language=book_details_dict["language"], average_rating=book_details_dict["average_rating"],
                                    categories=book_details_dict["categories"], thumbnail=book_details_dict["thumbnail"])
            db.session.add(book)
            db.session.commit()
        
        else:
            book = book_to_review

        review = request.form.get("review")
        user_id = session.get("user_id")
        user= crud.get_user_by_id(user_id)
        
        new_review = crud.create_review(user, book, review)

        return redirect(url_for("book_details", item_id=book_id_api))

        


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
