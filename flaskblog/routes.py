from flask import render_template, url_for, flash, redirect, request
from .forms import RegisterForm, LoginForm, UpdateAccountForm
from . import app, db, bcrypt
from .models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


#information of football players, each dictionary inside list contain data of one player
Footballers = [
    {
        'name': 'Jolin',
        'age': 21 ,
        'height': 175,
        'country': 'India'
    },

{
    'name': 'Grape',
    'age': 30,
    'height': 160,
    'country': 'Chinese-Canadian'
    },

{
    'name': 'Meow',
    'age': 22,
    'height': 165,
    'country': 'Usa'
    } ,

{
    'name': 'Adel',
    'age': 25,
    'height': 168,
    'country': 'Canada'
    } ,

{
    'name': 'Matt',
    'age': 22,
    'height': 178,
    'country': 'Canada'
    },

{
    'name': 'Mihir',
    'age': 26,
    'height': 174,
    'country': 'India'
    },

{
    'name': 'Ravi',
    'age': 27,
    'height': 172,
    'country': 'Indian-Canadian'
    }
]


# Define a route that maps the URL "/" (the root URL) to the following function
@app.route("/")
# Define a route that maps the URL "/home" (the home page URL) to the same function
@app.route("/home")
def hello():
    # This function will be triggered when someone accesses the root or home URL
    # It returns a response "Hello, Flask!" to the client (web browser)
    return render_template('home.html',  footballers = Footballers)

@app.route("/about")
def about_page():
    return render_template('about.html', footballers = Footballers)

@app.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        submit = form.submit.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
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
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
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

@app.route("/user_profile", methods = ['GET','POST'])
@login_required
def user_profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('user_profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('profile.html', title='Account', image_file = image_file, form=form)