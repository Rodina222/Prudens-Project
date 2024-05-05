from flask import Flask, render_template ,url_for ,flash, redirect, request
from datetime import datetime
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY']='962d4d203bdebe514e6a4856b2fa1730279bb814a3cfc3e720277662f98aa9fb'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///prudens.db'
db=SQLAlchemy(app)


# with app.app_context():
#     # Create all tables
#     db.create_all()



# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'mariam7tawfik@gmail.com'  # SMTP server address
app.config['MAIL_PORT'] = 587  # Port for SMTP
app.config['MAIL_USE_TLS'] = True  # Use TLS encryption
app.config['MAIL_USERNAME'] = ''  # Your email username
app.config['MAIL_PASSWORD'] = ''  # Your email password
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]
# Initialize Flask-Mail
mail = Mail(app)


from prudens import routes