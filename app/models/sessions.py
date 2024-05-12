from .database import db

class Session(db.Model):
    __tablename__ = 'sessions'
    sid = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    expiration = db.Column(db.DateTime)
