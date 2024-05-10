# app.py
from flask_sqlalchemy import SQLAlchemy
from .database import db
import datetime



 



class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    memberships = db.relationship('Membership', backref='member', lazy=True)

class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcfromtimestamp())
    active = db.Column(db.Boolean, default=True)  # Indicates if the membership is active
    duration = db.Column(db.Integer, nullable=False)  # Duration in months




