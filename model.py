from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

                    #  db.Column("user_id", db.Integer, db.ForeignKey("users.user_id"), primary_key=True),


book_users = db.Table("book_users", db.Column("book_id", db.Integer, db.ForeignKey("books.book_id"), primary_key=True),
            db.Column("bookshelf_id", db.Integer, db.ForeignKey("bookshelves.bookshelf_id"), primary_key=True))

class User(db.Model):
    """ A user """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(25), nullable = False)
    last_name = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique=True)
    password = db.Column(db.String(50), nullable = False)

    # book_users = db.relationship("Bookshelf", backref="bookshelf")
    # books = db.relationship("Book", secondary=book_users, lazy="subquery",
    #             backref=db.backref("user", lazy=True))

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

# tags = db.relationship('Tag', secondary=tags, lazy='subquery',
#         backref=db.backref('pages', lazy=True))


class Bookshelf(db.Model):
    """ Stores information about book the user wants to read"""   

    __tablename__ = "bookshelves"

    bookshelf_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id")) 
    # book_id = db.Column(db.Integer, db.ForeignKey("books.book_id")) 

    # book = db.relationship("Book", backref="bookshelves")
    user = db.relationship("User", backref="bookshelves")

    books = db.relationship("Book", secondary=book_users, lazy="subquery",
                backref=db.backref("bookshelf", lazy=True), overlaps="books,user")

    def __repr__(self):
        return f"<Bookshelf bookshelf_id={self.bookshelf_id} user_id={self.user_id}>"
    

class Review(db.Model):
    """ A review on a book """

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, primary_key = True, autoincrement = True)  
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id")) 
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id")) 
    review = db.Column(db.Text, nullable = False)

    book = db.relationship("Book", backref="reviews")
    user = db.relationship("User", backref="reviews")
    
    def __repr__(self):
        return f"<Review review_id={self.review_id} comment={self.comment}>"

# bookshelf3 = Bookshelf(user_id=user3.user_id, book_id=book3.book_id)

class Book(db.Model):
    """ A book """

    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key = True, autoincrement = True)  
    title = db.Column(db.String, nullable = False) 
    author = db.Column(db.String, nullable = False)

    # book_users = db.relationship("Book", backref="book")
    
    # bookshelves = db.relationship("Bookshelf", secondary=book_users, lazy="subquery",
    #             backref=db.backref("books", lazy=True))
    
    def __repr__(self):
        return f"<Book book_id={self.book_id} title={self.title} author={self.author}>"


# tags = db.Table('tags',
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
#     db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
# )





    # book_user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    # book_id = db.Column(db.Integer, db.ForeignKey("books.book_id")) 
    # user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    # bookshelf_id = db.Column(db.Integer, db.ForeignKey("bookshelves.bookshelf_id"))

    # book = db.relationship("Book", backref="book_users")
    # user = db.relationship("User", backref="book_users")
    # bookshelf = db.relationship("Bookshelf", backref="book_users")




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