from flask import Flask, render_template ,url_for ,flash, redirect, request
from forms import RegistrationForm , LoginForm
from datetime import datetime
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY']='962d4d203bdebe514e6a4856b2fa1730279bb814a3cfc3e720277662f98aa9fb'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///prudens.db'

db=SQLAlchemy(app)
# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'mariam7tawfik@gmail.com'  # SMTP server address
app.config['MAIL_PORT'] = 587  # Port for SMTP
app.config['MAIL_USE_TLS'] = True  # Use TLS encryption
app.config['MAIL_USERNAME'] = ''  # Your email username
app.config['MAIL_PASSWORD'] = ''  # Your email password

# Initialize Flask-Mail
mail = Mail(app)


@app.route('/')
def home():
    return render_template('signin.html')



@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_pass.html')


@app.route('/researcher_signup', methods=['GET', 'POST'])
def researcher_signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process the form data
        # Send verification email
        send_verification_email(form.email.data)

        # Flash a success message
        flash('Verification email sent! Please check your inbox.', 'success')
        return redirect(url_for('home'))

    # This part will execute only if the form is first loaded or did not pass validation
    # If form.errors is not empty, there were validation errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')

    return render_template('researcher_sign_up.html', form=form)

@app.route('/verify_email', methods=['GET'])
def verify_email():
    # This is a placeholder. You would typically handle the verification logic here.
    # For example, activate the user's account based on the verification token.
    return 'Email verified successfully!'


# Function to send verification email
def send_verification_email(email):
    verify_url = url_for('verify_email', _external=False)
    subject = 'Verify Your Account'
    body = f'Thank you for signing up! Please click the link below to verify your account:\n\n{verify_url}'
    msg = Message(subject=subject, recipients=[email], body=body)
    try:
        mail.send(msg)
    except Exception as e:
        print(e)  # Handle any exceptions here

if __name__ == '__main__':
    app.run(debug=True)




class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(25),nullable=False)
    lname=db.Column(db.String(25),nullable=False)
    username=db.Column(db.String(25),nullable=False,unique=True)
    email=db.Column(db.String(125),nullable=False,unique=True)
    password=db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"User('{self.fname}', '{self.lname}', '{self.username}', '{self.email}')"


