import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from .forms import RegisterForm, LoginForm, UpdateAccountForm, PostForm
from . import app, db, bcrypt
from .models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# Define a route that maps the URL "/" (the root URL) to the following function
@app.route("/")
# Define a route that maps the URL "/home" (the home page URL) to the same function
@app.route("/home")
def hello():
    # This function will be triggered when someone accesses the root or home URL
    # It returns a response "Hello, Flask!" to the client (web browser)
    posts = Post.query.all()
    return render_template('home.html',  posts=posts)

@app.route("/about")
def about_page():
    return render_template('about.html')

@app.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = RegisterForm()
    if form.validate_on_submit():  # if the form is validated according to the validators
        username = form.username.data # get the data from the form
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        submit = form.submit.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # hash the password
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {username}! you can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Registration', form=form)

@app.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated: # if the user is authenticated then redirect it to home page
        return redirect(url_for('hello'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        submit = form.submit.data
        user = User.query.filter_by(email=email).first() # get the user from the database
        if user and bcrypt.check_password_hash(user.password, password): # check if the user exists and password is correct
            # Log in the user after successful authentication
            login_user(user, remember=form.Remember.data) # This will keep the user logged in even after closing the browser
            return redirect(url_for('hello'))
        else:
            flash(f'Invalid Account', 'danger')
    return render_template('login.html', title='Login Page', form=form)

@app.route("/logout")
def logout():
    logout_user()  #  user is now not authenticated
    flash("You have been logged out.")
    return redirect(url_for('hello'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # generate a random hex
    _, fext = os.path.splitext(form_picture.filename) # get the file extension
    picture_fn = random_hex + fext # create a new file name with random hex and file extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    resize_img = Image.open(form_picture) # open the image
    resize_img.thumbnail(output_size) # resize the image

    resize_img.save(picture_path) # save the picture to the path created above and return the file name
    return picture_fn

@app.route("/user_profile", methods = ['GET','POST'])
@login_required # this decorator ensures that the user is logged in
def user_profile():
    form = UpdateAccountForm()
    if form.validate_on_submit(): # if the form is validated
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('user_profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('profile.html', title='Account', image_file = image_file, form=form)

@app.route("/post/new", methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('hello'))
    return render_template('create_post.html', title='New Post', form=form)