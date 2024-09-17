# from website import from __init__ the variable db
# ? __init__ is always accessible when its module is called
from . import db
# ! Flask-Login update isn't compatible with Werkzeug 3.0.
# ! This one is a known issue, i m forced to install older version
from flask_login import UserMixin
# To assign current date and time for notes
from sqlalchemy.sql import func



# ? SPECIAL CASE: for Users, we can inherit from UserMixin
# Users Table Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    # ? Key sensitive for relationship "Note"
    notes = db.relationship('Note')

# Notes Table Model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #Associate Note with User with foreign key
    # ? In this case one User can have many Notes (One to Many relation)
    # ? lowercase for ForeignKey "user"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Category_Book relation
category_book = db.Table('category_book', 
                         db.Column('book_id', db.Integer, db.ForeignKey('book.id')), 
                         db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
                        )
#Language_Book relation
category_book = db.Table('language_book', 
                         db.Column('book_id', db.Integer, db.ForeignKey('book.id')), 
                         db.Column('language_id', db.Integer, db.ForeignKey('language.id'))
                        )

# Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    price = db.Column(db.Integer)
    cover = db.Column(db.String(300))
    author = db.Column(db.String(300))
    description = db.Column(db.String(10000))
    pages = db.Column(db.Integer)

    categories = db.relationship('Category', secondary='category_book', backref='books')
    languages = db.relationship('Language', secondary='language_book', backref='books')

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

# Category Model
class Category(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    description = db.Column(db.String(10000))

# Author Model
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    description = db.Column(db.String(10000))

    books = db.relationship('Book')


# Language Model
class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))

# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    city = db.Column(db.String(100))
    adress = db.Column(db.String(500))
    books = db.Column(db.String(500))
    trackID = db.Column(db.Integer)