from app import db

class Address(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    line1 = db.Column(db.String(100))
    line2 = db.Column(db.String(100))
    city = db.Column(db.String(35))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(5))