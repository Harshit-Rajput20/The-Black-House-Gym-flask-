from datetime import datetime
from .database import db

class PackageSignupTable(db.Model):
    __tablename__ = 'package_signuptable'
    id = db.Column(db.Integer, primary_key=True)
    packagetype = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)

    # Define relationship with User table
    user = db.relationship('User', backref=db.backref('package_signups', lazy=True))

    def __init__(self, packagetype, date, user_email):
        self.packagetype = packagetype
        self.date = date
        self.user_email = user_email
