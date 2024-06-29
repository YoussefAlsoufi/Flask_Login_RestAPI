from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
class User(db.Model, UserMixin):
    __tablename__ = 'Users_creds' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    phone = db.Column(db.String(10), nullable=False, unique=True)
    role = db.Column(db.String(4), nullable=True)
    note = db.relationship('Note',backref='user', lazy = True, cascade='all, delete-orphan') # Lazy by default is 'Select' 

    def __repr__(self):
      return f"<User(email='{self.email}', first_name='{self.user_name}', phone='{self.phone}')>"


class Note (db.Model):
    __tablename__ = 'Notes'
    id = db.Column(db.Integer, primary_key= True)
    note_data = db.Column(db.String(1000))
    note_date = db.Column(db.DateTime(timezone = True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey ('Users_creds.id'))

    @property
    def formatted_date(self):
        return self.note_date.strftime('%Y-%m-%d %H:%M:%S')