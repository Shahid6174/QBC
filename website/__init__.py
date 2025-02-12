from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mailman import Mail


db = SQLAlchemy()
DB_NAME = "qbc.db"


def create_app():
    app = Flask(__name__)
    db.init_app()
    create_database(app)
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')