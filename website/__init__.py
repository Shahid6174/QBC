from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_mailman import Mail
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
mail = Mail()  

load_dotenv()

from .models import User

DB_NAME = os.environ.get('SQLITE_DB', 'qbc.db') 
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'qbc_admin@gmail.com') 
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '342b6h558h6z2w57')
SECRET_KEY = os.environ.get('SECRET_KEY', 'shahid')

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
                    password=generate_password_hash(
                        ADMIN_PASSWORD
                    ),
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
    print("Admin email address:", ADMIN_EMAIL)
    print("Admin password:", ADMIN_PASSWORD)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = ADMIN_EMAIL
    app.config['MAIL_PASSWORD'] = ADMIN_PASSWORD
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    
    db.init_app(app)
    mail.init_app(app)
    Migrate(app, db)
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login page if not authenticated

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Fetch user from the database

    from .views import views
    from .auth import auth
   
    app.register_blueprint(views, url_prefix="/")
   
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)
    
    return app
