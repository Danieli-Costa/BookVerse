from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# Table to connect book and bookshelf

book_users = db.Table("book_users", db.Column("book_id", db.Integer, db.ForeignKey("books.book_id"), primary_key=True),
                      db.Column("bookshelf_id", db.Integer, db.ForeignKey("bookshelves.bookshelf_id"), primary_key=True))


class User(db.Model):
    """ A user """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(30))

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"
    
    



class Bookshelf(db.Model):
    """ Stores information about book the user wants to read"""

    __tablename__ = "bookshelves"

    bookshelf_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref="bookshelves")

    books = db.relationship("Book", secondary=book_users, lazy="subquery",
                            backref=db.backref("bookshelf", lazy=True), overlaps="books,user")
    # bookshelf_status = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Bookshelf bookshelf_id={self.bookshelf_id} user_id={self.user_id}>"


class Review(db.Model):
    """ A review on a book """

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))
    review = db.Column(db.Text, nullable=False)

    book = db.relationship("Book", backref="reviews")
    user = db.relationship("User", backref="reviews")

    def __repr__(self):
        return f"<Review review_id={self.review_id} review={self.review}>"


class Book(db.Model):
    """ A book """

    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id_api = db.Column(db.Text)
    title = db.Column(db.String, nullable=False)
    subtitle = db.Column(db.String)
    authors = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    publisher = db.Column(db.String)
    published_date = db.Column(db.DateTime)
    page_count = db.Column(db.Integer)
    categories = db.Column(db.String)
    average_rating = db.Column(db.Float)
    ratings_count = db.Column(db.Integer)
    language = db.Column(db.String)
    thumbnail = db.Column(db.String)

    

    def __repr__(self):
        return f"<Book book_id={self.book_id} title={self.title} author={self.author}>"


def connect_to_db(flask_app, db_uri='postgresql:///bookshelf', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
