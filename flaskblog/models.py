from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from . import app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os

@login_manager.user_loader
def load(user_id):
    return User.query.get(int(user_id))

#Every model class inherits from db.Model,
# which tells Flask-SQLAlchemy that this class represents a database table.
class User(db.Model, UserMixin):  # Change db.model to db.Model
    # Each attribute of the class (e.g., username, id) corresponds to a column in the database table.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.image_file})'

    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(f"{os.environ.get('secret_key')}", expires_sec) #create a serializer object with secret key and expiration time
        return s.dumps({'user_id': self.id}).decode('utf-8') #return token as string

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(f"{os.environ.get('secret_key')}")
        try:
            user_id = s.loads(token)['user_id']
        except:
            return {'error': 'Invalid or expired token'}
        return User.query.get(user_id)

#Every model class inherits from db.Model, which tells Flask-SQLAlchemy that this class represents a database table.
class Post(db.Model):  # Change db.model to db.Model
    # Each attribute of the class (e.g., username, id) corresponds to a column in the database table.
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Also fix this line to use datetime.utcnow
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Post({self.title}, {self.date_posted})'
