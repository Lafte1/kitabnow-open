# Blueprint: Routes for user (login page, homepage...)
# render_template: HTML code and templates
# request: Handle requests (GET,POST...)
# flash: Flash messages
# redirect, url_for: for redirection to urls
from flask import Blueprint, render_template, request, flash, redirect, url_for
# Import database
from . import db
# Import User so we can add users to DB
from .models import User
# Password hash and check
from werkzeug.security import generate_password_hash, check_password_hash
# Flask login for users (UserMixin)
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

# Define authentication routes and methods they accept
# ? request.form >> form's data
# ? request.method >> http request type


@auth.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    # * Form submit button clicked
    if request.method == 'POST':
        # ? Get form data
        username = request.form.get('username')
        password = request.form.get('password')

        # ! Conditions check (form validation)
        if len(username) < 2:
            flash("Username too short", category='error')
        elif len(password) < 5:
            flash("Password too short", category='error')
            pass
        # ! Check if user exists in db
        else:
            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    # Login user
                    login_user(user, remember=True)
                    # Login success message
                    flash('Logged in Successfully!', category='success')
                    # Redirection to homepage
                    return redirect(url_for('admin_views.dashboard'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Username does not exist.', category='error')

    return render_template("admin/admin-login.html", user=current_user)



@auth.route('/admin-logout')
# ! LOGIN REQUITED to access LOGOUT
@login_required
def logout():
    #Logout the current user logged in using login_user()
    logout_user()
    return redirect(url_for('auth.admin_login'))


#Uncomment this to enable admin registration
"""
@auth.route('/admin-register', methods=['GET', 'POST'])
def admin_register():
    # * Form submit button clicked
    if request.method == 'POST':
        # ? Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        # ! Conditions check (form validation)
        if len(username) < 2:
            flash("Username is too short.", category='error')
        elif len(password) < 5:
            flash("Password is too short.", category='error')
            pass
        # ! Check if username already exists
        else:
            user = User.query.filter_by(username=username).first()
            if user:
                flash("Username already exists.", category='error')
            else:
                # Define user (prepare for DB)
                new_user = User(username=username, password=hashed_password)
                # Add user to db
                db.session.add(new_user)
                db.session.commit()
                #Login user
                login_user(new_user, remember=True)
                # Account creation flash message
                flash('Account successfully created!', category='success')
                # Redirection to homepage
                return redirect(url_for('admin_views.dashboard'))

    return render_template("admin/admin-register.html", user=current_user)
"""
