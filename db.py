from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# User class represents the base user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_type = db.Column(db.String(20), nullable=False)  # researcher, reviewer, admin

    __mapper_args__ = {
        'polymorphic_on': user_type
    }

# Researcher class represents researchers with additional attributes
class Researcher(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    field_of_study = db.Column(db.String(100), nullable=True)
    publications = db.relationship('Post', backref='author', lazy=True)  # One-to-many relationship with Post
    messages_sent = db.relationship('Message', backref='sender', lazy=True)  # One-to-many relationship with Message

    __mapper_args__ = {
        'polymorphic_identity': 'researcher'
    }

# Reviewer class represents reviewers with additional attributes
class Reviewer(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    expertise = db.Column(db.String(100), nullable=True)
    reviewed_posts = db.relationship('Post', backref='reviewer', lazy=True)  # One-to-many relationship with Post
    deleted_by_admin = db.relationship('Admin', backref='reviewer_deleted', lazy=True)  # One-to-many relationship with Admin

    __mapper_args__ = {
        'polymorphic_identity': 'reviewer'
    }

# Admin class represents administrators
class Admin(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    reviewers_deleted = db.relationship('Reviewer', backref='deleted_by_admin', lazy=True)  # One-to-many relationship with Reviewer

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

# Post class represents posts made by researchers
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('researcher.id'), nullable=False)  # Foreign key referencing Researcher
    reviewer_id = db.Column(db.Integer, db.ForeignKey('reviewer.id'))  # Foreign key referencing Reviewer
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, rejected
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy=True)  # One-to-many relationship with Comment
    reactions = db.relationship('React', backref='post', lazy=True)  # One-to-many relationship with React

# Notification class represents notifications sent to users
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Comment class represents comments on posts
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # Foreign key referencing Post
    content = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# React class represents reactions to posts
class React(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # Foreign key referencing Post
    reaction_type = db.Column(db.String(20), nullable=False)  