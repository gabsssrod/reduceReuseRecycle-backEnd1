from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return '<Users %r>' % self.first_name

    def serialize(self):
        return {
        "first_name": self.first_name,
        "last_name": self.last_name,
        "email": self.email,
        "password": self.password,
        }

class Objects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_name = db.Column(db.String(68), nullable=False)
    recycle = db.Column(db.String(68), nullable=False)
    reuse = db.Column(db.String(68), nullable=False)
    reduce = db.Column(db.String(68), nullable=False)

    def __repr__(self):
        return '<Objects %r>' % self.object_name

    def serialize(self):
        return {
            "id": self.id,
            "objectname": self.object_name,
            "recycle": self.recycle,
            "reuse": self.reuse,
            "reduce": self.reduce
        }
    
class Resource_Centers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    center_name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    website = db.Column(db.String(200), nullable=True)
    types = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Resource_Centers %r>' % self.center_name

    def serialize(self):
        return {
            "center_name": self.center_name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "hours": self.hours,
            "phone_number": self.phone_number,
            "website": self.website,
            "types": self.types
        }

class Days(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    first_day = db.Column(db.String(200), nullable=False)
    second_day = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Days %r>' % self.first_day

    def serialize(self):
        return {
            "first_day": self.first_day,
            "secon_day": self.secon_day
        }