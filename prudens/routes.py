from prudens.models import User, Researcher,NonResearcher, Reviewer, Admin, Post, Comment, React ,Follow,Message,Notification
from flask import Flask, render_template ,url_for ,flash, redirect, request
from prudens.forms import RegistrationForm , LoginForm,RegistrationForm_Non, PostForm, RequestResetForm, ResetPasswordForm
from prudens import app , bcrypt,db ,mail
import time
from sqlalchemy.exc import IntegrityError
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
    login_required,
)

from flask import session
from dotenv import load_dotenv  
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user


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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        
        
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            session['current_user_email'] = form.email.data  # Store user's email in session
        
            login_user(user, remember = form.remember.data)
            flash(f"You have been logged in successfully","success")

            if user.user_type=='reviewer':
                print('jhbhjhbj')
                posts = Post.query.filter_by(status='pending').all()
                print('after')
                return render_template('reviewer_gui.html', posts=posts)
            elif user.user_type=='researcher' or user.user_type=='non-researcher':
                form = PostForm()
                if form.validate_on_submit():
                    post_n = Post(
                        author_id=2,
                        reviewer_id=5,
                        title=form.label.data,
                        #refes=form.ref.data,
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
          flash(f"Login unsuccessful. Please check the credentials","danger")

    return render_template('signIn.html',form=form)



@app.route('/logout',methods=['GET'])
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
    return "Post Rejected Successfully"


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
    
    return render_template('add_post.html', form=form)

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
    flash("Post creation failed. Please check the form.", "danger")
    return render_template('add_post.html', form=form)


    
  

@app.route('/researchers')
def researchers():
    researchers = Researcher.query.all()
    return render_template('follow.html', researchers=researchers)



@app.route('/follow_researcher/<int:researcher_id>', methods=['POST'])
def follow_researcher(researcher_id):
    current_user_email = session.get('current_user_email')  # Retrieve user's email from session
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
        flash(f'You are already following {researcher.fname} {researcher.lname}.', 'info')
        return redirect(url_for('researchers'))

    # Create a new Follow relationship
    follow = Follow(follower_id=current_user.id, followed_id=researcher.id)
    db.session.add(follow)
    db.session.commit()

    flash(f'You are now following {researcher.fname} {researcher.lname}.', 'success')
    return redirect(url_for('researchers'))


@app.route('/unfollow_researcher/<int:researcher_id>', methods=['POST'])
def unfollow_researcher(researcher_id):
    current_user_email = session.get('current_user_email')  # Retrieve user's email from session
    if not current_user_email:
        flash('You must be logged in to follow researchers.', 'danger')
        return redirect(url_for('researchers'))

    researcher = Researcher.query.get_or_404(researcher_id)
    current_user = User.query.filter_by(email=current_user_email).first()

    # Check if the current user is already following the researcher
    existing_follow = Follow.query.filter_by(follower_id=current_user.id, followed_id=researcher.id).first()
    if existing_follow:
        # Delete the existing follow relationship
        db.session.delete(existing_follow)
        db.session.commit()
        flash(f'You have unfollowed {researcher.fname} {researcher.lname}.', 'info')
    else:
        flash(f'You are not following {researcher.fname} {researcher.lname}.', 'success')

    return redirect(url_for('researchers'))


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
