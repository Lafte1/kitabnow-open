#Blueprint: Routes for user (login page, homepage...)
#render_template: for HTML
from flask import Blueprint, render_template, request, flash, url_for, redirect
# Flask login for users (UserMixin)
from flask_login import login_required, current_user
from .models import Note, Book, Category, Language, Order, Author
from . import db
import json


admin_views = Blueprint('admin_views', __name__)

# * Whenever we go to '/dashboard' we execute what's inside: go to dashboard()
@admin_views.route('/dashboard', methods=['GET', 'POST'])
# ! LOGIN REQUITED to access homepage
@login_required
def dashboard():
    # * Add Note submit button clicked
    if request.method == 'POST':
        note = request.form.get('note')
        new_note = Note(data=note, user_id=current_user.id)
        # Add user to db
        db.session.add(new_note)
        db.session.commit()
        flash('Note added!', category='success')
    return render_template("admin/dashboard.html", user=current_user)


@admin_views.route('/cms', methods=['GET', 'POST'], defaults={"category_id":0})
@admin_views.route('/cms/<int:category_id>', methods=['GET', 'POST'])
@login_required
def cms(category_id):
    categories = Category.query.all()
    languages = Language.query.all()
    # * Add Book submit button clicked
    if request.method == 'POST':
        # ! Add book
        if 'add-book' in request.form:
            title = request.form.get('title')
            price = request.form.get('price')
            description = request.form.get('description')
            author = request.form.get('author')
            pages = request.form.get('pages')
            img = request.files['cover']

            if title == '' or price == '' or img.filename == '':
                flash('Please enter valid informations', category='error')
                return redirect(request.url)
            
            cover = img.filename

            
            save = '/home/kitabnow/htdocs/www.kitabnow.com/website/static/cms_books/'+cover

            #save = 'website/static/cms_books/'+cover
            img.save(save)

            selected_categories = request.form.getlist('category')
            selected_languages = request.form.getlist('language')

            book = Book.query.filter_by(title=title).first()
            if book:
                flash("تمت إضافة هذا الكتاب من قبل", category='info')
            else:
                check_author = Author.query.filter_by(name=author).first()
                if not check_author:
                    new_author = Author(name=author)
                    db.session.add(new_author)
                    db.session.commit()
                    
                author_id = Author.query.filter_by(name=author).first().id
                new_book = Book(title=title, price=price, cover=cover, author=author, description=description, pages=pages, author_id=author_id)

                for category in selected_categories:
                    new_book.categories.append(Category.query.filter_by(name=category).first())
                for language in selected_languages:
                    new_book.languages.append(Language.query.filter_by(name=language).first())

                db.session.add(new_book)
                db.session.commit()
                flash('تمت إضافة الكتاب بنجاح!', category='success')
        
        # ! Add Author
        elif 'add-author' in request.form:
            name = request.form.get('author')
            description = request.form.get('author_description')
            if name == '':
                flash('المرجو إدخال اسم مؤلف صحيح.', category='error')
                return redirect(request.url)

            author = Author.query.filter_by(name=name).first()
            if author:
                flash("تمت إضافة هذا المؤلف من قبل", category='info')
            else:
                new_author = Author(name=name, description=description)
                db.session.add_all([new_author])
                db.session.commit()
                flash('تمت إضافة المؤلف بنجاح!', category='success')

        
        # ! Add Category
        elif 'add-category' in request.form:
            name = request.form.get('category')
            description = request.form.get('description')
            if name == '':
                flash('Please enter valid category', category='error')
                return redirect(request.url)

            category = Category.query.filter_by(name=name).first()
            if category:
                flash("تمت إضافة هذا التصنيف من قبل", category='info')
            else:
                new_category = Category(name=name, description=description)
                db.session.add_all([new_category])
                db.session.commit()
                flash('تمت إضافة التصنيف بنجاح!', category='success')

        # ! Add Language
        elif 'add-language' in request.form:
            name = request.form.get('language')
            if name == '':
                flash('Please enter valid language', category='error')
                return redirect(request.url)

            language = Language.query.filter_by(name=name).first()
            if language:
                flash("تمت إضافة هذه اللغة من قبل", category='info')
            else:
                new_language = Language(name=name)
                db.session.add_all([new_language])
                db.session.commit()
                flash('تمت إضافة اللغة بنجاح!', category='success')
                return redirect(request.url)
    
    # ! Filter
    authors = Author.query.all()
    if category_id == 0:
        books=Book.query.all()
        return render_template("admin/cms.html", user=current_user, books=books,
                                categories=categories, languages=languages, authors=authors)
    else:
        category=Category.query.filter_by(id=category_id).first()
        return render_template("admin/cms.html", user=current_user, category=category,
                                categories=categories, languages=languages, authors=authors)
    

@admin_views.route('/delete-note', methods=['POST'])
def delete_note():
    data = json.loads(request.data)
    noteId = data['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return {}


@admin_views.route('/delete-book', methods=['POST'])
def delete_book():
    data = json.loads(request.data)
    bookId = data['bookId']
    book = Book.query.get(bookId)
    if book:
        db.session.delete(book)
        db.session.commit()
    return {}
    
@admin_views.route('/delete-author', methods=['POST'])
def delete_author():
    data = json.loads(request.data)
    authorId = data['authorId']
    author = Author.query.get(authorId)
    if author:
        db.session.delete(author)
        db.session.commit()
    return {}


@admin_views.route('/delete-category', methods=['POST'])
def delete_category():
    data = json.loads(request.data)
    categoryId = data['categoryId']
    category = Category.query.get(categoryId)
    if category:
        db.session.delete(category)
        db.session.commit()
    return {}


@admin_views.route('/delete-language', methods=['POST'])
def delete_language():
    data = json.loads(request.data)
    languageId = data['languageId']
    language = Language.query.get(languageId)
    if language:
        db.session.delete(language)
        db.session.commit()
        flash('Language deleted', category='info')
    return {}


@admin_views.route('/orders', methods=['GET', 'POST'])
# ! LOGIN REQUITED to access orders
@login_required
def orders():
    orders = Order.query.all()
    return render_template("admin/orders.html", user=current_user, orders=orders)


@admin_views.route('/editbook/<int:book_id>', methods=['GET', 'POST'])
# ! LOGIN REQUITED to access orders
@login_required
def editbook(book_id):
    book = Book.query.get_or_404(book_id)

    #* Edit Book submit button clicked
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        pages = request.form['pages']
        author = request.form['author']
        price = request.form['price']

        book.title = title
        book.description = description
        book.pages = pages
        book.author = author
        book.price = price

        db.session.add(book)
        db.session.commit()
        flash("تم تعديل كتاب "+book.title+" بنجاح", category='info')
        return redirect(url_for('admin_views.cms'))

    return render_template("admin/editbook.html", user=current_user, book=book)