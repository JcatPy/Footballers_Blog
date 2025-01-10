from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


#create an instance of a class flask
# __name__ variable(or argument) tells Flask where to find resource like template
app = Flask(__name__)

app.secret_key = f"{os.environ.get('secret_key')}" # secret key for the app
csrf = CSRFProtect(app) # Initialize the CSRFProtect object


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'   # SQLite database URI
db = SQLAlchemy(app)     # Initialize the database object
bcrypt = Bcrypt(app)   # Initialize the Bcrypt object
login_manager = LoginManager(app) # login manager which handles all the sessions and cookies
login_manager.login_view = 'login' # login route

from . import routes

