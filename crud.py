"""CRUD operations."""

from model import connect_to_db, User, Bookshelf, Review, Book


def create_user(email, password, first_name, last_name):
    """Create and return a new user"""

    user = User(email=email, password=password,
                first_name=first_name, last_name=last_name)

    return user


def get_users():
    """Returns all users"""

    return User.query.all()


def get_user_by_id(user_id):
    """Returns a user by the primary key"""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email"""

    return User.query.filter(User.email == email).first()


def create_book(title, author):
    """Create and return a book"""

    book = Book(title=title, author=author)

    return book


def get_books():
    """Returns all books"""

    return Book.query.all()


def get_book_by_id(book_id):
    """Returns a book by primaru key"""

    return Book.query.get(book_id)


def create_review(user, book, review):
    """Create a return a review"""

    review = Review(user=user, book=book, review=review)

    return review


def get_reviews_by_book_id(book_id):
    """Returns all reviews in a book"""

    return Review.query.filter_by(Review.book_id == book_id)


def create_bookshelf(user):
    """Create and return a bookshelf"""

    bookshelf = Bookshelf(user=user)

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


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
