
from db import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin): ##database model for users
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True) ##id is an integer column 
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    image_file = db.Column(db.String(20), default='default.jpg')
    about_user = db.Column(db.String(140))
    posts = db.relationship('Post', backref='owner') ##ralation to the posts table
    comments = db.relationship('Comment', backref='owner') ##ralation to the comments table
    
class Post(db.Model): ##database model for posts
    id = db.Column(db.Integer, primary_key=True) ##id is an integer column 
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime,  default=datetime.utcnow) ##automatically set the date column to the current time
    user_pk = db.Column(db.Integer, db.ForeignKey('user.id')) ##foreign key to the user table
    comments = db.relationship('Comment', backref='post') ##ralation to the comments table

class Comment(db.Model): ##database model for comments
    id = db.Column(db.Integer, primary_key=True) ##id is an integer column 
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime,  default=datetime.utcnow) ##automatically set the date column to the current time
    user_pk = db.Column(db.Integer, db.ForeignKey('user.id')) ##foreign key to the user table
    post_id = db.Column(db.Integer, db.ForeignKey('post.id')) ##foreign key to the post table