from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'you will never guess'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)    # Initializes database

    # Import blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models
    from .models import User, Note

    # Create database if it doesn't exist
    with app.app_context():
        db.create_all()

    # Login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'    # Redirects user to login page if they try to access a page that requires them to be logged in
    login_manager.init_app(app)    # Initializes login manager

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # Returns user with matching id

    return app





