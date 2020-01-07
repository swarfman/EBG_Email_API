from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True)
    emails = db.relationship('Email', backref='user', lazy='dynamic')

    def to_dict(self):
        temp_array = []
        for e in self.emails:
            temp_array.append(e.to_dict_simple_email())   
        return { 
          "id": self.id, 
          "name": self.name,
          "username": self.username,
          "password": self.password,
          "emails": temp_array
        }

    def __repr__(self):
        return '<User {}>'.format(self.name)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    email_type = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict_simple_email(self):
        return {
            "body": self.body,
            "id": self.id,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "email_type": self.email_type
        }