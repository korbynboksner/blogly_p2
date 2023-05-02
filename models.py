"""Models for Blogly."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User."""

    __tablename__ = "users"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                     nullable=False)
    last_name = db.Column(db.Text,
                     nullable=False)
    image_url = db.Column(db.Text,
                     nullable=False,
                     )
    post = db.relationship('Post', backref='user', cascade="all, delete-orphan")  
    
class Post(db.Model):
    """Post."""
    __tablename__ = "posts"
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.Text,
                    nullable=False)
    content = db.Column(db.Text,
                    nullable=False)
    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.id'),
                    nullable=False)             
    date = db.Column(db.Text,
                    nullable=False)
    u = db.relationship('User')

class Tag(db.Model):
    """Tag Model"""

    ___tablename___ = "tag"
    posts = db.relationship('Post',
                            secondary='post_tag',
                            cascade="all,delete",
                            backref='tag')
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.Text,
                    nullable=False,
                    unique=True)

    

class PostTag(db.Model):
    """Post==>Tag"""
    ___tablename___ = "post_tag"
    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tag.id'),
                        primary_key=True)

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)