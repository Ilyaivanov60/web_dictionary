from flask import Blueprint, request, redirect, render_template, flash, url_for
from flask_login import current_user, login_user, logout_user

from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.db import db

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        print('1')
        return redirect(url_for('word.index'))
    form = LoginForm()
    title = 'Авторизация'
    return render_template('user/login.html', page_title=title, form=form)

@blueprint.route('/process_login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('вы успешно вошли на сайт')
            return redirect(url_for('word.index'))

    flash('неправильный имя или пароль')
    return redirect(url_for('user.login'))

@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогины')
    return redirect(url_for('word.index'))



@blueprint.route('/registration')
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('word.index')) 
    else:
        form_reg = RegistrationForm()
        title = "Регистрация"
        return render_template('user/registration.html', page_title=title, form=form_reg)

@blueprint.route('/process_reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('word.index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле {}: - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
        return redirect(url_for('user.registration'))