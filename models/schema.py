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
    role = db.Column(db.Integer,default=3) # 1=admin,2=developer, 3=guest


class ExamLink(db.Model):
    exid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    link = db.Column(db.String(50))

class Number(db.Model):
    numid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    number = db.Column(db.Integer,unique=True)

