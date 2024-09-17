from flask import Flask
#import DB module
from flask_sqlalchemy import SQLAlchemy
# We'll use path to check if db exists
from os import path
from flask_login import LoginManager

# Declaration of a SQLALCHEMY db
db = SQLAlchemy()
# Database name
DB_NAME = "database.db"


#Setup/Init Flask Application
def create_app():
    app = Flask(__name__)
    #Encrypt cookies and session data
    app.config['SECRET_KEY'] = 'sekret cey'
    #Assign Location of SQLALCHEMY database and give it a name
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #Link db with app
    db.init_app(app)

    #Register Blueprints
    from .admin_views import admin_views
    from .auth import auth
    from .general_views import general_views
    app.register_blueprint(admin_views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(general_views, url_prefix='/')

    # Import models to define the User and Note models before creating db
    from .models import User, Note, Book, Category, Language, Order, Author

    #Create DB
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.admin_login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Create DB (function)
def create_database(app):
    from .models import User, Note, Book, Category, Language, Order, Author
    print("Creating database...")
    with app.app_context():
        db.create_all()
        print('Database created!')
