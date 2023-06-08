"""CRUD operations."""

from model import connect_to_db, User, Bookshelf, Review, Book, db
import datetime


def create_user(email, password, first_name, last_name, username):
    """Create and return a new user"""

    user = User(email=email, password=password,
                first_name=first_name, last_name=last_name, username=username)

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_id(user_id):
    """Returns a user by the primary key"""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email"""

    return User.query.filter(User.email == email).first()

def get_user_by_username(username):
    """Return a user by username"""

    return User.query.filter(User.username == username).first()


def create_book(book_id_api, title, subtitle, authors, publisher, published_date, page_count, language, average_rating, categories, thumbnail):
    """Create and return a book"""
    
    if len(published_date) == 4:
        date_obj = datetime.datetime.strptime(published_date, "%Y")
        print(date_obj)
    else:
        date_obj = datetime.datetime.strptime(published_date, "%Y-%m-%d")

    book = Book(book_id_api=book_id_api, title=title, subtitle=subtitle, authors=authors, publisher=publisher, published_date=date_obj,
                page_count=page_count, language=language, average_rating=average_rating, categories=categories, thumbnail=thumbnail)

    db.session.add(book)
    db.session.commit()

    return book



def get_book_by_id(book_id):
    """Returns a book by primaru key"""

    return Book.query.get(book_id)

def get_book_by_api_id(book_id_api):
    """Returns a book by the api id"""

    return Book.query.filter(Book.book_id_api == book_id_api).first()


def create_review(user, book, review):
    """Create a return a review"""

    review = Review(user=user, book=book, review=review)

    db.session.add(review)
    db.session.commit()

    return review


def get_reviews_by_api_id(book_id_api):
    """ Returns the reviews made on a book by the book api id """

    return Book.query.filter(Book.book_id_api == book_id_api).first().reviews


def create_bookshelf(user):
    """Create and return a bookshelf"""

    bookshelf = Bookshelf(user=user)

    db.session.add(bookshelf)
    db.session.commit()

    return bookshelf


def get_bookshelf_by_user_id(user_id):
    """Returns a bookshelf by the user_id"""

    return Bookshelf.query.get(user_id)


def add_books_in_bookshelf(user_id, book_id):
    """Add a book to a bookshelf"""

    bookshelf = get_bookshelf_by_user_id(user_id)
    book = get_book_by_id(book_id)

    bookshelf.books.append(book)

    return bookshelf


def get_books_in_a_bookshelf(user_id):
    """Returns all books in a bookshelf"""

    bookshelf = get_bookshelf_by_user_id(user_id)

    return bookshelf.books

def delete_book_from_bookshelf(bookshelf, book):
    """ Removes a book from a bookshelf """

    
    bookshelf.books.remove(book)

    db.session.commit()



if __name__ == "__main__":
    from server import app

    connect_to_db(app)
