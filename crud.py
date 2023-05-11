"""CRUD operations."""

from model import db, connect_to_db, User, Bookshelf, Review, Book


def create_user(email, password, first_name, last_name):
    """Create and return a new user"""

    user = User(email=email, password=password,
                first_name=first_name, last_name=last_name)

    return user


def create_book(title, author):
    """Create and return a book"""

    book = Book(title=title, author=author)

    return book


def create_review(user, book, review):
    """Create a return a review"""

    review = Review(user=user, book=book, review=review)

    return review


def create_bookshelf(user):
    """Create and return a bookshelf"""

    bookshelf = Bookshelf(user=user)

    return bookshelf


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
