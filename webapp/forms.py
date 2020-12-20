from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm the password', validators=[DataRequired()])
    email = StringField('Your email', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit_in = SubmitField('Log in')
    submit_out = SubmitField('Log out')
    confirm = SubmitField('confirm')


class WordForm(FlaskForm):
    confirm = SubmitField('Перевести')
    word_for_translate = StringField('Введите слово для перевода', validators=[DataRequired()])
