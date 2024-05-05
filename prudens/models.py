from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from prudens import db


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    registered_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_type = Column(String(20), nullable=False)  # researcher, reviewer, admin
    
    comments = db.relationship('Comment', backref='user')
    reacts = db.relationship('React', backref='user')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)


    __mapper_args__ = {
        'polymorphic_on': user_type
    }
    def __repr__(self):
        return f"User('{self.fname}','{self.lname}','{self.id}', '{self.username}', '{self.email}', '{self.registered_on}', '{self.user_type}')"

class Researcher(User):
    __tablename__ = 'researcher'  # Specify the table name for the Researcher class
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # Foreign key referencing User
    field_of_study = db.Column(db.String(100), nullable=True)
    publications = db.relationship('Post', backref='author', lazy=True)  # One-to-many relationship with Post
    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.registered_on}', '{self.field_of_study}')"

    __mapper_args__ = {
        'polymorphic_identity': 'researcher'
    }

class NonResearcher(User):

    __tablename__ = 'non-researcher' 
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # Foreign key referencing User

    __mapper_args__ = {
        'polymorphic_identity': 'non-researcher'
    }
    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.registered_on}')"

class Reviewer(User):
    __tablename__ = 'reviewer' 
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # Foreign key referencing User
    expertise = db.Column(db.String(100), nullable=True)
    reviewed_posts = db.relationship('Post', backref='reviewer', lazy=True)  # One-to-many relationship with Post

    __mapper_args__ = {
        'polymorphic_identity': 'reviewer'
    }


class Admin(User):
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # Foreign key referencing User
    __tablename__ = 'admin' 
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('researcher.id'), nullable=False)  # Foreign key referencing Researcher
    reviewer_id = db.Column(db.Integer, db.ForeignKey('reviewer.id'))  # Foreign key referencing Reviewer
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, rejected
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ########### Relations
    comments = db.relationship('Comment', backref='post')
    reacts = db.relationship('React', backref='post')
    def __repr__(self):
        return f"User('{self.id}', '{self.title}', '{self.content}', '{self.author_id}', '{self.reviewer_id}','{self.status}','{self.created_on}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # Foreign key referencing Post
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key referencing User
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"Comment('{self.id}', '{self.content}', '{self.post_id}', '{self.user_id}', '{self.created_on}')"

class React(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # Foreign key referencing Post
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key referencing User
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"React('{self.id}', '{self.post_id}', '{self.user_id}', '{self.created_on}')"

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"Message('{self.id}', '{self.sender_id}', '{self.recipient_id}', '{self.content}','{self.sent_on}')"

