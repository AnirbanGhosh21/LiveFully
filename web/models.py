from textblob.en import subjectivity
from .import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    password = db.Column(db.String(150))
    dateCreated = db.Column(db.DateTime(timezone=True), default=func.now())
    logs = db.relationship('Log', backref='user', passive_deletes=True)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    dateCreated = db.Column(db.DateTime(timezone=True), default=func.now())
    tags = db.Column(db.String(200), default='')
    polarity = db.Column(db.Float, default=0.0)
    subjectivity = db.Column(db.Float, default=0.0)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
