from db import db
from flask_login import UserMixin
from sqlalchemy import ForeignKey
# from sqlalchem.sql import func


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.String(80), nullable=False)
    user_role = db.relationship('UserRole', cascade="all,delete", backref="user")

class UserRole(db.Model):
    urid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    role = db.Column(db.Integer) # 1=admin,2=developer, 3=guest
