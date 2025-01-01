# Import the FlaskForm class from Flask-WTF, which provides functionality for form handling in Flask
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms.fields.simple import TextAreaField

from .models import User
# Import specific form field types (StringField, PasswordField, SubmitField) and validators (DataRequired, Email, Length, EqualTo)
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed #for uploading profile picture


# Define a class 'LoginForm' that inherits from FlaskForm. This class represents the registration form.
class RegisterForm(FlaskForm):
    # Define a 'username' field of type StringField (a text input field).
    # Validators:
    # - DataRequired(): Ensures that this field is not left empty.
    # - Length(min=2, max=20): Ensures that the input length is between 2 and 20 characters.
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    # Define an 'email' field of type StringField.
    # Validators:
    # - Email(): Ensures the input is in a valid email format (e.g., user@example.com).
    email = StringField('Email', validators=[DataRequired(), Email()])

    # Define a 'password' field of type PasswordField (a field for password input, obscured for privacy).
    password = PasswordField('Password', validators=[DataRequired()])

    # Define a 'confirm_password' field of type PasswordField (for confirming password input).
    # Validators:
    # - EqualTo('password'): Ensures that the value entered matches the 'password' field value (for password confirmation).
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    # Define a 'submit' field of type SubmitField (a button to submit the form).
    submit = SubmitField('Register')

    def validate_username(self, username):
        #check if the username already exists
        user_username = User.query.filter_by(username = username.data).first()
        if user_username:
            raise ValidationError('That username already exist')

    def validate_email(self, email):
        #check if the email already exists
        user_email = User.query.filter_by(email = email.data).first()
        if user_email:
            raise ValidationError('That email address already exist')

class LoginForm(FlaskForm):
    # This is a login form when users have already registered
    #we will use email instead of username to login
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    #this field helps to login again  when browser is closed and then it is opened again
    Remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    # only jpg and png files are allowed
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        #if the username is not same as the current user's username
        if self.username.data != current_user.username:
            user_username = User.query.filter_by(username=username.data).first()
            if user_username:
                raise ValidationError('That username already exist')

    def validate_email(self, email):
        if self.email.data != current_user.email:
            user_email = User.query.filter_by(email=email.data).first()
            if user_email:
                raise ValidationError('That email address already exist')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')