import os
from flask import Flask, render_template ,url_for ,flash, redirect, request
from datetime import datetime
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY']='962d4d203bdebe514e6a4856b2fa1730279bb814a3cfc3e720277662f98aa9fb'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///prudens.db'
db=SQLAlchemy(app)
bcrypt = Bcrypt()

login_manager =  LoginManager(app)

# Configure Flask-Mail
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')

app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
# app.config['MAIL_USE_SSL'] = True

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]
# Initialize Flask-Mail
mail = Mail(app)
mail.smtp_ssl = True


from prudens import routes