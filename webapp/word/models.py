from webapp.db import db


class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    original_word = db.Column(db.String(30))
    translatted_word = db.Column(db.String(140))

    def __repr__(self):
        return f"{self.original_word}: {self.translatted_word}: id={self.id}"
