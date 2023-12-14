from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    passw = db.Column(db.String(150))
    reg_date = db.Column(db.DateTime(timezone=True), default=func.now())
    contact = db.relationship('Contacts')


class Contacts(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    type = db.Column(db.String(150))
    phone = db.Column(db.String(150))
    email = db.Column(db.String(150))
    com = db.Column(db.String(150))
    pic_name = db.Column(db.String(150))
    pic_path = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



