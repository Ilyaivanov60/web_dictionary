from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class lessonForm(FlaskForm):
    create = SubmitField('Создать', render_kw={"class": "btn btn-primary"})
