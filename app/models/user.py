# user.py
from flask_sqlalchemy import SQLAlchemy
from .database import db
import datetime

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    memberships = db.relationship('Membership', backref='member', lazy=True)

    def add_membership(self, duration):
        # Get the last active membership, if any
        last_membership = Membership.query.filter_by(member_id=self.id, active=True).order_by(Membership.end_date.desc()).first()

        # Calculate start date for the new membership
        start_date = datetime.datetime.utcnow()
        if last_membership:
            start_date = last_membership.end_date + datetime.timedelta(days=1)

        # Calculate end date for the new membership
        end_date = start_date + datetime.timedelta(days=duration * 30)  # Assuming duration is in months

        # Create and add the new membership
        new_membership = Membership(member_id=self.id, start_date=start_date, end_date=end_date, duration=duration)
        db.session.add(new_membership)
        db.session.commit()

class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    membership_type = db.Column(db.String(100), nullable=False)  # Type of membership
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, default=True)  # Indicates if the membership is active
    duration = db.Column(db.Integer, nullable=False)  # Duration in months
