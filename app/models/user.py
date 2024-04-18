# app.py
from flask_sqlalchemy import SQLAlchemy
from .database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=True, nullable=False)
    middlename = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    password_hash = db.Column(db.Text, nullable=False)
    email_verified = db.Column(db.Boolean, default=False) 
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    signup_date = db.Column(db.DateTime, nullable=False)
    package_type = db.Column(db.Integer, default=0)
    last_package_date = db.Column(db.DateTime)



    def set_password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __init__(self, firstname,middlename,lastname, email, phone_number, signup_date):
        self.firstname = firstname
        self.middlename = middlename
        self.lastname= lastname
        self.email = email
        self.phone_number = phone_number
        self.signup_date = signup_date
        # self.package_type = package_type
        # self.last_package_date = last_package_date

# Example of creating a new User object
# new_user = User(username='john_doe', email='john@example.com', phone_number='1234567890', signup_date=datetime.now())
