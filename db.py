

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_db(app): 
    db.init_app(app) ##initialized db

    with app.app_context():
        db.create_all() ##create database