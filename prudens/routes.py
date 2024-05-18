from prudens.models import User, Researcher, NonResearcher, Reviewer, Admin, Post, Comment, React, Follow, Message, Notification, Issue
from flask import Flask, render_template, url_for, flash, redirect, request
from prudens.forms import RegistrationForm, LoginForm, RegistrationForm_Non, PostForm, support_form
from prudens import app, bcrypt, db, mail
import time
import sqlite3
from sqlalchemy.exc import IntegrityError
from flask_mail import Message
from flask_login import login_user
from flask import session
from dotenv import load_dotenv
import yagmail


@app.route('/')
@app.route('/home')
def home():
    form = LoginForm()
    return render_template('signIn.html', form=form)


@app.route('/researcher_signup', methods=['GET', 'POST'])
def researcher_signup():
    try:
        form = RegistrationForm()
        if form.validate_on_submit():
            # Process the form data
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')

            researcher = Researcher(
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
            flash(
                f"Account created successfully for {form.username.data}", "success")
            time.sleep(5)
            return redirect(url_for('home'))
    except IntegrityError as e:
        db.session.rollback()  # Rollback the session to prevent changes
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
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
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

            flash(
                f"Account created successfully for {form.username.data}", "success")
            return redirect(url_for('home'))
        except IntegrityError as e:
            db.session.rollback()  # Rollback the session to prevent changes
            if 'email' in str(e):
                flash(
                    'Email is already registered. Please use another email address.', 'error')
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


@app.route('/settings')
def settings():
    # Retrieve user information from the database based on the email
    # Replace with the logged-in user's email
    email = 's-mariam.abouzaid@zewailcity.edu.eg'
    user = User.query.filter_by(email=email).first()
    return render_template('settings.html', user=user)


@app.route('/support', methods=['GET', 'POST'])
def support():
    form = support_form()
    if form.validate_on_submit():
        Issue_n = Issue(
                content = form.problem.data
            )
        print(Issue_n.content)
        db.session.add(Issue_n)
        db.session.commit()
    return render_template('support.html', form=form)

@app.route('/profile')
def profile():
    current_user_email = session.get('current_user_email')
    print(current_user_email)
    user = User.query.filter_by(email=current_user_email).first()
    print(user.id)
    posts = Post.query.filter_by(author_id=user.id).filter_by(status='approved').all()
    print(posts)
    return render_template('profile.html', posts=posts)

@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    print(post_id)
    notification_to_delete = Notification.query.filter_by(post_id=post_id).first()
    db.session.delete(notification_to_delete)
    db.session.commit()
    
    post_to_delete = Post.query.filter_by(id=post_id).first()
    db.session.delete(post_to_delete)
    db.session.commit()
    current_user_email = session.get('current_user_email')
    user = User.query.filter_by(email=current_user_email).first()
    posts = Post.query.filter_by(author_id=user.id).filter_by(status='approved').all()
    return render_template('profile.html', posts=posts)

@app.route('/Edit_post/<int:post_id>')
def Edit_post(post_id):
    current_user_email = session.get('current_user_email')
    user = User.query.filter_by(email=current_user_email).first()
    posts = Post.query.filter_by(author_id=user.id).filter_by(status='approved').all()
    return render_template('profile.html', posts=posts)

@app.route('/update_fname', methods=['POST'])
def update_fname():
    # Retrieve form data
    # Replace with the logged-in user's email
    email = 's-mariam.abouzaid@zewailcity.edu.eg'
    user = User.query.filter_by(email=email).first()
    user.fname = request.form['fname']
    # Commit the changes to the database
    db.session.commit()
    return 'User information updated successfully'


@app.route('/update_lname', methods=['POST'])
def update_lname():
    # Retrieve form data
    # Replace with the logged-in user's email
    email = 's-mariam.abouzaid@zewailcity.edu.eg'
    user = User.query.filter_by(email=email).first()
    user.fname = request.form['lname']
    # Commit the changes to the database
    db.session.commit()
    return 'User information updated successfully'


@app.route('/delete_account', methods=['POST'])
def delete_account():
    # Retrieve user's email from session
    current_user_email = session.get('current_user_email')
    print(current_user_email)
    user_to_delete = User.query.filter_by(email=current_user_email).first()
    print(user_to_delete)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Store user's email in session
            session['current_user_email'] = form.email.data

            login_user(user, remember=form.remember.data)
            flash(f"You have been logged in successfully", "success")

            if user.user_type == 'reviewer':
                print('jhbhjhbj')
                posts = Post.query.filter_by(status='pending').all()
                print('after')
                return render_template('reviewer_gui.html', posts=posts)
            elif user.user_type == 'researcher':
                form = PostForm()
                if form.validate_on_submit():
                    post_n = Post(
                        author_id=2,
                        reviewer_id=5,
                        title=form.label.data,
                        # refes=form.ref.data,
                        content=form.post.data,
                        status='pending')

                    db.session.add(post_n)
                    db.session.commit()
                    # Flash a success message
                    flash(
                        f"post created successfully for {form.label.data}", "success")
                    time.sleep(5)
                    return render_template('Created ')

                return render_template('add_post.html', form=form)

            else:
                return ('Hello , Login successfully')

        else:
            flash(f"Login unsuccessful. Please check the credentials", "danger")

    return render_template('signIn.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    # current_user_email = session.get('current_user_email')
    # session.pop(current_user_email, None)  # Remove user's email from session
    session.pop('current_user_email', None)  # Remove user's email from session
    print(current_user_email)
    form = LoginForm()
    return render_template('signIn.html', form=form)


@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_pass.html')


@app.route('/reviewer_gui')
def reviewer_gui():
    # Fetch pending posts from the database
    posts = Post.query.filter_by(status='pending').all()
    return render_template('reviewer_gui.html', posts=posts)


@app.route('/review_post/<int:post_id>', methods=['POST'])
def review_post(post_id):
    # Logic to handle review of the post
    feedback = request.form.get('feedback')
    post = Post.query.get_or_404(post_id)
    post.status = 'approved'
    db.session.commit()
    return "Post Reviewed Successfully"


@app.route('/reject_post/<int:post_id>', methods=['POST'])
def reject_post(post_id):
    # Logic to handle rejection of the post
    reason = request.form.get('reason')
    post = Post.query.get_or_404(post_id)
    post.status = 'rejected'
    db.session.commit()
    return "Post Rejected Successfully"


@app.route('/researchers')
def researchers():
    researchers = Researcher.query.all()
    return render_template('follow.html', researchers=researchers)


@app.route('/follow_researcher/<int:researcher_id>', methods=['POST'])
def follow_researcher(researcher_id):
    # Retrieve user's email from session
    current_user_email = session.get('current_user_email')
    if not current_user_email:
        flash('You must be logged in to follow researchers.', 'danger')
        return redirect(url_for('researchers'))
    researcher = Researcher.query.get_or_404(researcher_id)
    current_user = User.query.filter_by(email=current_user_email).first()

    if current_user.id == researcher.id:
        flash('You cannot follow yourself.', 'danger')
        return redirect(url_for('researchers'))
    # Check if the current user is already following the researcher
    if Follow.query.filter_by(follower_id=current_user.id, followed_id=researcher.id).first():
        flash(
            f'You are already following {researcher.fname} {researcher.lname}.', 'info')
        return redirect(url_for('researchers'))

    # Create a new Follow relationship
    follow = Follow(follower_id=current_user.id, followed_id=researcher.id)
    db.session.add(follow)
    db.session.commit()

    flash(
        f'You are now following {researcher.fname} {researcher.lname}.', 'success')
    return redirect(url_for('researchers'))


@app.route('/unfollow_researcher/<int:researcher_id>', methods=['POST'])
def unfollow_researcher(researcher_id):
    # Retrieve user's email from session
    current_user_email = session.get('current_user_email')
    if not current_user_email:
        flash('You must be logged in to follow researchers.', 'danger')
        return redirect(url_for('researchers'))

    researcher = Researcher.query.get_or_404(researcher_id)
    current_user = User.query.filter_by(email=current_user_email).first()

    # Check if the current user is already following the researcher
    existing_follow = Follow.query.filter_by(
        follower_id=current_user.id, followed_id=researcher.id).first()
    if existing_follow:
        # Delete the existing follow relationship
        db.session.delete(existing_follow)
        db.session.commit()
        flash(
            f'You have unfollowed {researcher.fname} {researcher.lname}.', 'info')
    else:
        flash(
            f'You are not following {researcher.fname} {researcher.lname}.', 'success')

    return redirect(url_for('researchers'))
