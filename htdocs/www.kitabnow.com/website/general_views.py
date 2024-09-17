from flask import Blueprint, render_template, request, flash, jsonify, json
from .models import Category, Book, Order
from . import db
import random


general_views = Blueprint('general_views', __name__)

# ! Home page:
@general_views.route('/', methods=['GET', 'POST'])
def home():
    categories = Category.query.all()
    return render_template("general/home.html", categories=categories)

@general_views.route('/filter', methods=['POST'])
def filter():
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        selected = Category.query.filter_by(id=category_id).first()
        books = selected.books  # Assuming selected.books is a list of book objects

        # Convert the list of book objects to a list of dictionaries
        books_list = []
        number = 0
        for book in books:
            if number <=3:
                number += 1
                books_list.append({
                    "title": book.title,
                    "price": book.price,
                    "cover": book.cover
                    # Add more book properties here
                })
                
        return jsonify({
            "id": selected.id,
            "name": selected.name,
            "description": selected.description,
            "books": books_list  # Send the list of dictionaries
        })
    

# ! Shop page:
@general_views.route('/categories', methods=['GET', 'POST'])
def categories():
    return render_template("general/categories.html")

@general_views.route('/getcategories', methods=['POST'])
def getcategories():
    if request.method == 'POST':
        categories = Category.query.all()
        categories_dict = []
        for category in categories:
            books_dict = []
            for book in category.books:
                books_dict.append({
                    "id": book.id,
                    "title": book.title,
                    "price": book.price,
                    "cover": book.cover
                    # Add more book properties here
                })
            categories_dict.append({
                    "id": category.id,
                    "name": category.name,
                    "description": category.description,
                    "books": books_dict
                    # Add more book properties here
                })
        
        return jsonify({
            "categories": categories_dict
        })

@general_views.route('/category/<category_name>', methods=['GET', 'POST'])
def category(category_name):
    category = Category.query.filter_by(name=category_name).first()
    all_categories = Category.query.with_entities(Category.id, Category.name)
    return render_template("general/category.html", category=category, all_categories=all_categories)


# ! Book individual page:
@general_views.route('/book/<book_title>', methods=['GET', 'POST'])
def book(book_title):
    book = Book.query.filter_by(title=book_title).first()
    return render_template("general/book.html", book=book)


# ! Cart page:
@general_views.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template("general/cart.html")

@general_views.route('/cartbooks', methods=['POST'])
def cartBooks():
    if request.method == 'POST':
        # Retrieve the JSON data from the request body
        data = request.get_json()
        booksIds = json.loads(data)

        cartbooks = []
        for bookId in booksIds:
            # Get book from db by id
            book = Book.query.filter_by(id=bookId).first()
                
            cartbooks.append({
                "id": book.id,
                "title": book.title,
                "price": book.price,
                "cover": book.cover,
                "quantity": booksIds[bookId],
                # Add more book properties here
                })
            
        # Return a JSON response without redirection
        return jsonify({
            "cartbooks": cartbooks
        })
    

# ! Checkout page:
@general_views.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Get order infos
        fname = request.form.get('fname')
        phone = request.form.get('phone')
        city = request.form.get('city')
        adress = request.form.get('adress')
        orderbooks = request.form.get('orderbooks')
        trackID = random.randint(100000,100000000)

        new_order = Order(fname=fname, phone=phone, city=city, adress=adress, books=orderbooks, trackID=trackID)
        # Add order to db
        db.session.add(new_order)
        db.session.commit()
        return render_template("general/order_success.html")

    return render_template("general/checkout.html")


# ! Order sucess page:
@general_views.route('/order_success', methods=['GET', 'POST'])
def order_success():
    return render_template("general/order_success.html")