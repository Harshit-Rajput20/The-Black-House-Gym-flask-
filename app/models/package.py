from .database import db

class PackageSignupTable(db.Model):
    __tablename__ = 'package_signuptable'
    id = db.Column(db.Integer, primary_key=True)
    packagetype = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)

    def __init__(self, packagetype, date, email):
        self.packagetype = packagetype
        self.date = date
        self.email = email