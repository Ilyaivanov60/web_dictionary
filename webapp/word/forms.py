from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class WordForm(FlaskForm):
    submit = SubmitField('Перевести', render_kw={"class": "btn btn-primary"})
    word_for_translate = StringField('Введите слово для перевода', validators=[DataRequired()], render_kw={"class": "form-control"})
    transleted_word = StringField('Перевод', render_kw={"class": "form-control"})
    add = SubmitField('Добавить', render_kw={"class": "btn btn-primary"})
    edit = SubmitField('Редактировать', render_kw={"class": "btn btn-primary"})
    delete = SubmitField('Удалить', render_kw={"class": "btn btn-primary"})
