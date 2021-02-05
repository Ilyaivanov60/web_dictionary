from webapp.db import db


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    word_id = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.original_word}: {self.translatted_word}: id={self.id}"