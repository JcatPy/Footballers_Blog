#from Tools.scripts.make_ctype import method
from flask import Flask
#from pandas.conftest import nullable_string_dtype
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#create an instance of a class flask
# __name__ variable(or argument) tells Flask where to find resource like template
app = Flask(__name__)

app.secret_key = 'da213f3bdb5a55f14a5b2481a509ceea'
csrf = CSRFProtect(app) # Initialize the CSRFProtect object

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'   # SQLite database URI
db = SQLAlchemy(app)     # Initialize the database object
bcrypt = Bcrypt(app)   # Initialize the Bcrypt object
login_manager = LoginManager(app) # login manager which handles all the sessions and cookies
login_manager.login_view = 'login' # login route

from . import routes

