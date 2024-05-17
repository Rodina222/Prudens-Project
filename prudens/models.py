from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from prudens import db,app
from prudens import  login_manager
from flask_login import UserMixin
from itsdangerous import URLSafeSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class Follow(db.Model):
    __tablename__ = 'follow'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    def __repr__(self):
        return f"Follow('{self.follower_id}', '{self.followed_id}')"


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Message('{self.content}', '{self.timestamp}', '{self.sender_id}', '{self.receiver_id}')"


class User(db.Model,UserMixin):
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
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], backref='followed', lazy='select')
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref='follower', lazy='select')


       # Relationship with messages sent by the user
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)

    # Relationship with messages received by the user
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)



    __mapper_args__ = {
        'polymorphic_on': user_type
    }

    def get_reset_token(self):
        serializer= Serializer(app.config['SECRET_KEY'], salt = 'pw-reset')
        return serializer.dumps({'user_id': self.id})
    
    @staticmethod 
    def verify_reset_token(token, age = 3600):  # reset password is valid for 1 hour
        serializer= Serializer(app.config['SECRET_KEY'], salt = 'pw-reset')

        try:
             user_id = serializer.loads(token , max_age = age)['user_id']
        
        except:
            return None
        
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.fname}','{self.lname}','{self.id}', '{self.username}', '{self.email}', '{self.registered_on}', '{self.user_type}')"

class Researcher(User):
    __tablename__ = 'researcher'  # Specify the table name for the Researcher class
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # Foreign key referencing User
    field_of_study = db.Column(db.String(100), nullable=False)
    linkedin_account = db.Column(db.String(150), nullable=False)
    google_scholar_account =db.Column(db.String(150), nullable=False)
    

    publications = db.relationship('Post', backref='author', lazy=True)  # One-to-many relationship with Post

 

    __mapper_args__ = {
        'polymorphic_identity': 'researcher'
    
    }

    

class NonResearcher(User):

    __tablename__ = 'non-researcher' 
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # Foreign key referencing User

    __mapper_args__ = {
        'polymorphic_identity': 'non-researcher'
    }

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


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    recipient_id = db.Column(db.Integer,db.ForeignKey('researcher.id'), nullable=False)  # ID of the recipient user
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # ID of the related post
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    recipient = db.relationship('Researcher', backref='notifications')  # Define the relationship with Researcher

    def __repr__(self):
        return f"Notification('{self.message}', '{self.recipient_id}', '{self.post_id}', '{self.created_on}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('researcher.id'), nullable=False)  # Foreign key referencing Researcher
    reviewer_id = db.Column(db.Integer, db.ForeignKey('reviewer.id'))  # Foreign key referencing Reviewer
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, rejected
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    feedback =db.Column(db.Text)
    ########### Relations
    comments = db.relationship('Comment', backref='post')
    reacts = db.relationship('React', backref='post')
    def __repr__(self):
        return f"Post('{self.id}', '{self.title}', '{self.content}', '{self.author_id}', '{self.reviewer_id}','{self.status}','{self.created_on}','{self.feedback}')"