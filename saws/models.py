from sqlalchemy.orm import backref
from . import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String)
    email = db.Column(db.String)

    account = db.relationship('Account', backref='users', uselist=False)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
        
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')


class Account(db.Model):

    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    access_key = db.Column(db.String)
    secret_key = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
