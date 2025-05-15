from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_mailman import Mail
from flask_migrate import Migrate
from flask_babel import Babel
from werkzeug.security import generate_password_hash
from datetime import timedelta

db = SQLAlchemy()
mail = Mail()
babel = Babel()

load_dotenv()

from .models import User

# Default values for development
DB_NAME = os.environ.get('SQLITE_DB', 'qbc.db')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'qbc_admin@fastmail.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin@123')
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-123')

@babel.localeselector
def get_locale():
    # Try to get the language from the session
    return session.get('language', 'en')

def create_database(app):
    with app.app_context():
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            print("Created Database!")

            # Check if admin user already exists
            admin_user = User.query.filter_by(email=ADMIN_EMAIL).first()
            if not admin_user:
                print("Creating default admin user...")
                admin = User(
                    email=ADMIN_EMAIL,
                    password=generate_password_hash(ADMIN_PASSWORD),
                    full_name="Admin QBC",
                    is_admin=True,
                    is_verified=True
                )
                db.session.add(admin)
                db.session.commit()
                print("Admin user created!")
        else:
            print("Database already exists!")

def create_app():
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Session configuration
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Email configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = ADMIN_EMAIL
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-mail-password')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = ADMIN_EMAIL
    
    # Babel configuration
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'translations')
    app.config['LANGUAGES'] = {
        'en': 'English',
        'sw': 'Kiswahili'
    }
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    migrate = Migrate(app, db)
    babel.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Create database
    create_database(app)
    
    return app
