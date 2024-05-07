from prudens.models import User, Researcher,NonResearcher, Reviewer, Admin, Post, Comment, React
from flask import Flask, render_template ,url_for ,flash, redirect, request
from prudens.forms import RegistrationForm , LoginForm,RegistrationForm_Non
from prudens import app , bcrypt,db ,mail
import time
import sqlite3
from sqlalchemy.exc import IntegrityError
from flask_mail import  Message


@app.route('/')
def home():
    return render_template('signIn.html')



@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_pass.html')


@app.route('/researcher_signup', methods=['GET', 'POST'])
def researcher_signup():
    try:
        form = RegistrationForm()
        if form.validate_on_submit():
            # Process the form data
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            researcher=Researcher(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            field_of_study=form.field_of_study.data,
            linkedin_account=form.linkedin_account.data,
            google_scholar_account=form.google_scholar_account.data
            )

            db.session.add(researcher)
            db.session.commit()
            # Flash a success message
            flash(f"Account created successfully for {form.username.data}", "success")
            time.sleep(5)
            return redirect(url_for('home'))
    except IntegrityError as e:
        db.session.rollback()  # Rollback the session to prevent changes
        if 'email' in str(e):
            flash('Email is already registered. Please use another email address.', 'error')
        elif 'username' in str(e):
            flash('Username is not unique. Please choose another username.', 'error')
        else:
            flash('An error occurred. Please try again later.', 'error')

        return redirect(url_for('researcher_signup'))



    # This part will execute only if the form is first loaded or did not pass validation
    # If form.errors is not empty, there were validation errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')

    return render_template('researcher_sign_up.html', form=form)



@app.route('/non_researcher_signup', methods=['GET', 'POST'])
def non_researcher_signup():
    form = RegistrationForm_Non()
    if form.validate_on_submit():
        try:
            # Process the form data
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            non_researcher = NonResearcher(
                fname=form.fname.data,
                lname=form.lname.data,
                username=form.username.data,
                email=form.email.data,
                password=hashed_password
            )

            db.session.add(non_researcher)
            db.session.commit()
            # Flash a success message
            msg = Message('Hello', sender='mariam7tawfik@gmail.com', recipients=[form.email.data])
            msg.body = "Hello sonal my first mail app"
            mail.send(msg)

            flash(f"Account created successfully for {form.username.data}", "success")
            return redirect(url_for('home'))
        except IntegrityError as e:
            db.session.rollback()  # Rollback the session to prevent changes
            if 'email' in str(e):
                flash('Email is already registered. Please use another email address.', 'error')
            elif 'username' in str(e):
                flash('Username is not unique. Please choose another username.', 'error')
            else:
                flash('An error occurred. Please try again later.', 'error')
            return redirect(url_for('non_researcher_signup'))

    return render_template('non_researcher_sign_up.html', form=form)



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


@app.route('/settings')
def settings():
    # Retrieve user information from the database based on the email
    email = 's-mariam.abouzaid@zewailcity.edu.eg'  # Replace with the logged-in user's email
    user = User.query.filter_by(email=email).first()
    return render_template('settings.html', user=user)






@app.route('/update_fname', methods=['POST'])
def update_fname():
    # Retrieve form data
    email = 's-mariam.abouzaid@zewailcity.edu.eg'  # Replace with the logged-in user's email
    user = User.query.filter_by(email=email).first()
    user.fname = request.form['fname']
    # Commit the changes to the database
    db.session.commit()
    return 'User information updated successfully'

@app.route('/update_lname', methods=['POST'])
def update_lname():
    # Retrieve form data
    email = 's-mariam.abouzaid@zewailcity.edu.eg'  # Replace with the logged-in user's email
    user = User.query.filter_by(email=email).first()
    user.fname = request.form['lname']
    # Commit the changes to the database
    db.session.commit()
    return 'User information updated successfully'

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    
    if request.method == 'POST':
        # Handle form submission
        username = request.form.get('username')
        password = request.form.get('password')
        return render_template('reviewer_gui.html')

    #     if username == '' and password == '':
    #         # If both username and password are empty, render a different template
    #         return render_template('reviewer_gui.html')
    #     else:
    #         # Render the sign-in page with an error message
    #         return render_template('signIn.html', error='Invalid username or password')
    # else:
    #     # Render the sign-in page for GET requests
    #     return render_template ('signIn.html',error=None)
