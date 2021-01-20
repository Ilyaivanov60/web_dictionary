from flask_login import UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.db import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password )

    def __repr__(self):
        return '<User name={} id={}>'.format(self.username, self.id)


class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_word = db.Column(db.String(30))
    translatted_word = db.Column(db.String(140))

    def __repr__(self):
        return '<Word={} traslatted={}>'.format(self.original_word, self.translatted_word)