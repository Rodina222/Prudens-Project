<<<<<<< HEAD
from prudens.models import User, Researcher,NonResearcher, Reviewer, Admin, Post, Comment, React ,Follow,Message,Notification
from flask import Flask, render_template ,url_for ,flash, redirect, request
from prudens.forms import RegistrationForm , LoginForm,RegistrationForm_Non, PostForm, RequestResetForm, ResetPasswordForm, RegistrationForm_Reviewer
from prudens import app , bcrypt,db ,mail
=======
from prudens.models import User, Researcher, NonResearcher, Reviewer, Admin, Post, Comment, React, Follow, Message, Notification, Issue
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from prudens.forms import RegistrationForm, LoginForm, RegistrationForm_Non, PostForm, RequestResetForm, ResetPasswordForm, support_form
from prudens import app, bcrypt, db, mail
>>>>>>> 07bc80e7f3cc733a528b46002270829c7d471c4c
import time
from datetime import datetime
import base64

from sqlalchemy.exc import IntegrityError
<<<<<<< HEAD
from werkzeug.security import generate_password_hash
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
    login_required,
)

=======
>>>>>>> 07bc80e7f3cc733a528b46002270829c7d471c4c
from flask import session
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from prudens.repositories import UserRepository   ,NonResearcherRepository,ResearcherRepository

import yagmail


@app.route('/')
def home():
    form = LoginForm()
    return render_template('signIn.html', form=form)

@app.route('/home')
def home_page():
    # Fetch pending posts from the database
    posts = Post.query.all()
    if not posts:
      #  message = "There are no posts yet! Follow other users and see their posts."
        return render_template('home_page.html')
      # Fetch author information for each post
    for post in posts:
        author = User.query.get(post.author_id)
        post.author_first_name = author.fname
        post.author_last_name = author.lname
    
    return render_template('home_page.html', posts=posts,current_page='home_page')
 

@app.route('/researcher_signup', methods=['GET', 'POST'])
def researcher_signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Process the form data
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            
            researcher = ResearcherRepository.create_researcher(
                fname=form.fname.data,
                lname=form.lname.data,
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                field_of_study=form.field_of_study.data,
                linkedin_account=form.linkedin_account.data,
                google_scholar_account=form.google_scholar_account.data
            )

            # Flash a success message
            flash(f"Account created successfully for {form.username.data}", "success")
            time.sleep(5)
            return redirect(url_for('home'))
        except IntegrityError as e:
            db.session.rollback()  # Rollback the session to prevent changes
            flash('An error occurred. Please try again later.', 'error')
            return redirect(url_for('researcher_signup'))

    # Handle validation errors
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
            
            non_researcher = NonResearcherRepository.create_non_researcher(
                fname=form.fname.data,
                lname=form.lname.data,
                username=form.username.data,
                email=form.email.data,
                password=hashed_password
            )

            # Flash a success message
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



@app.route('/notification')
@login_required
def notification():
    # Fetch approved or rejected posts for the current user
    approved_rejected_posts = Post.query.filter_by(author_id=current_user.id).filter(Post.status.in_(['approved', 'rejected'])).all()
    
    # Create notifications for approved or rejected posts if they don't exist
    for post in approved_rejected_posts:
        existing_notification = Notification.query.filter_by(recipient_id=current_user.id, post_id=post.id).first()
        if not existing_notification:
            message = f"Your post '{post.title}' has been {post.status}."
            if post.status == 'rejected':
                feedback = post.feedback
                message += f" Feedback: {feedback}"
            notification = Notification(
                message=message,
                recipient_id=current_user.id,
                post_id=post.id,
                created_on=datetime.utcnow()
            )
            db.session.add(notification)
    db.session.commit()

    # Fetch unique notifications for the current user including feedback from the associated post
    notifications = []
    for notification in Notification.query.filter_by(recipient_id=current_user.id).distinct(Notification.post_id).all():
        post = Post.query.get(notification.post_id)
        notifications.append({
            'message': notification.message,
            'created_on': notification.created_on,
            'feedback': post.feedback if post else None  # Fetch feedback from associated post
        })

    return render_template('notification.html', notifications=notifications)
# Add a route for handling the back button redirection
@app.route('/back_to_add_post')
def back_to_add_post():
    return redirect(url_for('add_post.html'), code=302)

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
    if notification_to_delete:
        print(notification_to_delete)
        db.session.delete(notification_to_delete)
        db.session.commit()
    
    post_to_delete = Post.query.filter_by(id=post_id).first()
    if post_to_delete:
        print(post_to_delete)
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
@login_required
def update_fname():
    # Retrieve current user's email from Flask-Login's current_user
    current_user_email = current_user.email

    # Update the user's first name
    new_fname = request.form['fname']
    user = UserRepository.update_fname(current_user_email, new_fname)
    
    if user:
        flash("First name updated successfully", "success")
    else:
        flash("User not found", "danger")

    return redirect(url_for('settings'))

@app.route('/update_lname', methods=['POST'])
@login_required
def update_lname():
    # Retrieve current user's email from Flask-Login's current_user
    current_user_email = current_user.email

    # Update the user's last name
    new_lname = request.form['lname']
    user = UserRepository.update_lname(current_user_email, new_lname)
    
    if user:
        flash("Last name updated successfully", "success")
    else:
        flash("User not found", "danger")

    return redirect(url_for('settings'))



@app.route('/delete_account', methods=['POST'])
def delete_account():
    # Retrieve user's email from session
    current_user_email = session.get('current_user_email')
    if not current_user_email:
        # Handle the case where there is no current user email in the session
        flash("No user logged in", "danger")
        return redirect(url_for('home'))

    # Delete the user by email
    User_k = UserRepository.get_by_email(current_user_email)
    
    followers = Follow.query.filter_by(follower_id=User_k.id)
    followeds = Follow.query.filter_by(followed_id=User_k.id)
    posts = Post.query.filter_by(author_id=User_k.id)
    
    for follower in followers:
        db.session.delete(follower)
        db.session.commit()
        
    for followed in followeds:
        db.session.delete(followed)
        db.session.commit()
        
    for post in posts:
        db.session.delete(post)
        db.session.commit()
        
    user_to_delete = UserRepository.delete_by_email(current_user_email)
    
    if user_to_delete:
        flash("Account deleted successfully", "success")
    else:
        flash("Account not found", "danger")

    return redirect(url_for('home'))




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
<<<<<<< HEAD
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            if user.user_type == 'admin':
                session['current_user_email'] = form.email.data  # Store user's email in session
                login_user(user, remember=form.remember.data)
                return redirect(url_for('admin_dashboard'))

            if user.user_type == 'reviewer':
                session['current_user_email'] = form.email.data  # Store user's email in session
                login_user(user, remember=form.remember.data)
                posts = Post.query.filter_by(status='pending').all()
                return render_template('reviewer_gui.html', posts=posts)

            if bcrypt.check_password_hash(user.password, form.password.data):
                session['current_user_email'] = form.email.data  # Store user's email in session
                login_user(user, remember=form.remember.data)
                flash("You have been logged in successfully", "success")

                if user.user_type == 'researcher' or user.user_type == 'non-researcher':
                    form = PostForm()
                    if form.validate_on_submit():
                        post_n = Post(
                            author_id=2,
                            reviewer_id=5,
                            title=form.label.data,
                            content=form.post.data,
                            status='pending')

                        db.session.add(post_n)
                        db.session.commit()
                        flash(f"Post created successfully for {form.label.data}", "success")
                        time.sleep(5)
                        return render_template('Created')

                    return render_template('add_post.html', form=form)
                else:
                    return "Hello, Login successfully"
            else:
                flash("Login unsuccessful. Please check the credentials", "danger")
       
=======
        user = UserRepository.get_by_email(form.email.data)

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Store user's email in session
            session['current_user_email'] = form.email.data

            login_user(user, remember=form.remember.data)
            flash(f"You have been logged in successfully", "success")

            if user.user_type == 'reviewer':
                
                posts = Post.query.filter_by(status='pending').all()
                
                return render_template('reviewer_gui.html', posts=posts)
            elif user.user_type=='researcher' or user.user_type=='non-researcher':
                
                return redirect(url_for("home_page"))
            
            else:
                return ('Hello , Login successfully')

        else:
            flash(f"Login unsuccessful. Please check the credentials", "danger")

    return render_template('signIn.html', form=form)
>>>>>>> 07bc80e7f3cc733a528b46002270829c7d471c4c

    return render_template('signIn.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('current_user_email', None)  # Remove user's email from session
    current_user_email = session.get('current_user_email')  # Retrieve user's email from session
    print(current_user_email)
    form = LoginForm()
    return render_template('signIn.html', form=form)


@app.route('/forgot_password', methods=['GET', 'POST'])
def reset_request():

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash(
                "If this account exists, you will receive an email with instructions",
                "info",
            )
            # Redirect to the reset password page with the email as a query parameter
            return redirect(url_for("reset_password", email=form.email.data))
        
        else:
            flash("User not found", "error")
            return redirect(url_for("login"))

    return render_template('reset_request.html', title="Reset Request", form=form)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    email = request.args.get('email')  # Retrieve email from query parameter
    if not email:
        flash("Email not provided", "error")
        return redirect(url_for("reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        print("Form validated")
        user = User.query.filter_by(email=email).first()
        #print("New password:", form.password.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated successfully for {user.email}", "success")
       # print("Password updated for user:", user.email)
        return redirect(url_for("login"))
          
    return render_template('reset_password.html', title="Reset Password", form=form)

@app.route('/reviewer_gui')  # Make sure this route is defined
def reviewer_gui():
    # Fetch pending posts from the database
    posts = Post.query.filter_by(status='pending').all()
    if not posts:
        message = "There are no pending posts. All of them are reviewed."
        return render_template('reviewer_gui.html', message=message)
    return render_template('reviewer_gui.html', posts=posts)


@app.route('/review_post/<int:post_id>', methods=['POST'])
def review_post(post_id):
    # Logic to handle review of the post
    post = Post.query.get_or_404(post_id)
    
    # Check if feedback is provided
    feedback = request.form.get('feedback')
    
    if not feedback:
        flash("Please provide feedback, if not write N/A.", "warning")
        return redirect(url_for('reviewer_gui'))
    
    post.feedback = feedback
    post.status = 'approved'
    db.session.commit()
    flash("Post approved successfully", "success")  # Flash message for successful approval
    return redirect(url_for('reviewer_gui'))


@app.route('/reject_post/<int:post_id>', methods=['POST'])
def reject_post(post_id):
    # Logic to handle rejection of the post
    post = Post.query.get_or_404(post_id)
    
    # Check if feedback is provided
    feedback = request.form.get('feedback')
    
    if not feedback:
        flash("Please provide feedback, if not write N/A.", "warning")
        return redirect(url_for('reviewer_gui'))
    
    post.feedback = feedback
    post.status = 'rejected'
    db.session.commit()
    flash("Post rejected successfully", "success")  # Flash message for successful approval
    return redirect(url_for('reviewer_gui'))


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        current_user_email = session.get('current_user_email')  # Retrieve user's email from session
        current_user = User.query.filter_by(email=current_user_email).first()
        if current_user:
            post_n = Post(
                author_id=current_user.id,
                title=form.label.data,
                content=form.post.data,
                status='pending',
                reference=form.ref.data  # Add this line to assign the ref attribute
            )
            db.session.add(post_n)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('add_post'))
        else:
            flash('User not found.', 'danger')
    else:
        # Print validation errors for debugging
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
        flash("Post creation failed. Please check the form.", "danger")
    
    return render_template('add_post.html', form=form,current_page='add_post')


@app.route('/settings')
def settings():
    # Retrieve user information from the database based on the email
    current_user_email = session.get('current_user_email')  # Retrieve user's email from session
    user = User.query.filter_by(email=current_user_email).first()
    return render_template('setting.html', user=user,current_page='settings')
   


@app.route('/follow_researcher/<int:researcher_id>', methods=['POST'])
def follow_researcher(researcher_id):
    # Retrieve user's email from session
    current_user_email = session.get('current_user_email')
    if not current_user_email:
        flash('You must be logged in to follow researchers.', 'danger')
        return redirect(url_for('home_page'))
    researcher = Researcher.query.get_or_404(researcher_id)
    current_user = User.query.filter_by(email=current_user_email).first()

    if current_user.id == researcher.id:
        flash('You cannot follow yourself.', 'danger')
        return redirect(url_for('home_page'))
    # Check if the current user is already following the researcher
    if Follow.query.filter_by(follower_id=current_user.id, followed_id=researcher.id).first():
        flash(
            f'You are already following {researcher.fname} {researcher.lname}.', 'info')
        return redirect(url_for('home_page'))

    # Create a new Follow relationship
    follow = Follow(follower_id=current_user.id, followed_id=researcher.id)
    db.session.add(follow)
    db.session.commit()

    flash(
        f'You are now following {researcher.fname} {researcher.lname}.', 'success')
    return redirect(url_for('home_page'))


@app.route('/unfollow_researcher/<int:researcher_id>', methods=['POST'])
def unfollow_researcher(researcher_id):
    # Retrieve user's email from session
    current_user_email = session.get('current_user_email')
    if not current_user_email:
        flash('You must be logged in to follow researchers.', 'danger')
        return redirect(url_for('home_page'))

    researcher = Researcher.query.get_or_404(researcher_id)
    current_user = User.query.filter_by(email=current_user_email).first()

    # Check if the current user is already following the researcher
    existing_follow = Follow.query.filter_by(
        follower_id=current_user.id, followed_id=researcher.id).first()
    if current_user.id == researcher.id:
        flash('You cannot unfollow yourself.', 'danger')
        return redirect(url_for('home_page'))
    elif existing_follow:
        # Delete the existing follow relationship
        db.session.delete(existing_follow)
        db.session.commit()
        flash(
            f'You have unfollowed {researcher.fname} {researcher.lname}.', 'info')
    else:
        flash(
            f'You are not following {researcher.fname} {researcher.lname}.', 'success')

    return redirect(url_for('home_page'))


#@app.route('/')
@app.route('/send_message', methods=['GET', 'POST'])
@login_required

def send_message():
    if request.method == 'POST':
        receiver_email = request.form.get('email')
        print(receiver_email)
        sender_email = session.get('current_user_email')  # Retrieve user's email from session
        content = request.form.get('message')
        print(content)
        receiver = User.query.filter_by(email=receiver_email).first()
        sender = User.query.filter_by(email=sender_email).first()

        if not receiver:
            flash('Receiver not found.', 'danger')
        elif sender_email == receiver_email:
            flash('You cannot send a message to yourself.', 'danger')
        else:
            try:
                new_message = Message(content=content, sender_id=sender.id, receiver_id=receiver.id)
                print(f"Message instance created: {new_message}")
            except Exception as e:
                print(f"Error creating message instance: {e}")

            # Add and commit the new message to the database
            try:
                db.session.add(new_message)
                db.session.commit()
                flash('Your message has been sent!', 'success')
            except Exception as e:
                print(f"Error committing message to database: {e}")
                flash('Failed to send message', 'danger')
            return redirect(url_for('send_message'))

    return render_template('send_message.html',current_page='send_message')


@app.route('/sent_messages')
@login_required
def sent_messages():
    current_user_email = session.get('current_user_email')  # Retrieve user's email from session
    current_user = User.query.filter_by(email=current_user_email).first()
    messages_sent = Message.query.filter_by(sender_id=current_user.id).all()
    # Fetch receiver names based on receiver_id
    receiver_names = {}
    receiver_emails = {}
    for message in messages_sent:
        receiver_id = message.receiver_id
        receiver = User.query.filter_by(id=receiver_id).first()
        receiver_names[receiver_id] = receiver.fname+' '+receiver.lname 
        receiver_emails[receiver_id] = receiver.email

    return render_template('sent_messages.html', messages_sent=messages_sent, receiver_names=receiver_names, receiver_emails=receiver_emails,current_page='sent_messages')


@app.route('/received_messages')
@login_required
def received_messages():
    current_user_email = session.get('current_user_email')  # Retrieve user's email from session
    current_user = User.query.filter_by(email=current_user_email).first()
    # Query messages received by the current user
    messages_received = Message.query.filter_by(receiver_id=current_user.id).all()
    sender_names = {}
    sender_emails = {}
    for message in messages_received:
        sender_id = message.sender_id
        sender = User.query.filter_by(id=sender_id).first()
        sender_names[sender_id] = sender.fname + ' ' + sender.lname
        sender_emails[sender_id] = sender.email
    print(messages_received)
    return render_template('received_messages.html', messages_received=messages_received, sender_names=sender_names, sender_emails=sender_emails,current_page='received_messages')


@app.route('/reply_message', methods=['POST'])
@login_required
def reply_message():
    print('reply')
    if request.method == 'POST':
        current_user_email = session.get('current_user_email')
        current_user = User.query.filter_by(email=current_user_email).first()

        receiver_id = request.form.get('receiver_id')
        message_content = request.form.get('message_content')

        new_message = Message(content=message_content, sender_id=current_user.id, receiver_id=receiver_id)
        db.session.add(new_message)
        db.session.commit()

        # Redirect to the sent messages page or any other page as needed
        return redirect(url_for('sent_messages'))

    # Redirect to the sent messages page if the request method is not POST
    return redirect(url_for('sent_messages'))

<<<<<<< HEAD
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    form = RegistrationForm_Reviewer()
    if form.validate_on_submit():
        try:
            reviewer = Reviewer(
                fname=form.fname.data,
                lname=form.lname.data,
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.add(reviewer)
            db.session.commit()
            flash('Account created successfully!', 'success')
        except Exception as e:
            flash('An error occurred while creating the account. Please try again later.', 'error')
            app.logger.error('Error creating reviewer: %s', str(e))
            db.session.rollback()  # Rollback changes if an error occurs
    else:
        print("Form errors:", form.errors)  # Print form validation errors
    return render_template('admin.html', form=form)
=======
@app.route('/search_posts', methods=['POST'])
def search_posts():
    data = request.get_json()
    search_query = data.get('query', '').strip()
    
    if search_query:
        search_pattern = f"%{search_query}%"
        matching_posts = Post.query.filter(Post.content.ilike(search_pattern)).all()
        
        results = []
        for post in matching_posts:
            author = User.query.get(post.author_id)
            highlighted_content = post.content.replace(search_query, f"<mark>{search_query}</mark>")
            results.append({
                'author_first_name': author.fname,
                'author_last_name': author.lname,
                'content': highlighted_content
            })
        
        return jsonify(results)
    
    return jsonify([])
>>>>>>> 07bc80e7f3cc733a528b46002270829c7d471c4c

