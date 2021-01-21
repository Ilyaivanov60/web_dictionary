from flask import Flask, redirect, render_template, flash, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_migrate import Migrate

from get_translated_word import get_translation
from webapp.db import db
from webapp.model import User, Cards
from webapp.forms import LoginForm, RegistrationForm, WordForm


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    @app.route('/index')
    def index():
        title = "Домашная страница"
        return render_template('index.html', page_title=title)

    @app.route('/word')
    def word():
        title = "Переводчик"
        cards_db = Cards.query.filter(Cards.user_id==current_user.get_id()).all()
        word_form = WordForm()
        if current_user.is_authenticated:
            return render_template('word.html', page_title=title, cards=cards_db, form=word_form)
        else:
            flash('вы не вошли на сайт')
            return redirect(url_for('login'))

    @app.route('/word_process', methods=["POST"])
    def word_process():
        form = WordForm()
        word_exist_in_db = Cards.query.filter(Cards.original_word==form.word_for_translate.data).count()
        if not word_exist_in_db:
            if form.validate_on_submit():
                user_id = current_user.get_id()
                new_word = Cards(original_word=form.word_for_translate.data, translatted_word=get_translation(form.word_for_translate.data), user_id=user_id)
                db.session.add(new_word)
                db.session.commit()
                flash('Вы успешно добавили слово!')
                return redirect(url_for('word'))
        else:
            flash('слово уже в db')
            return redirect(url_for('word'))

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        title = 'Авторизация'
        return render_template('login.html', page_title=title, form=form)

    @app.route('/process_login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('вы успешно вошли на сайт')
                return redirect(url_for('index'))

        flash('неправильный имя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогины')
        return redirect(url_for('index'))



    @app.route('/registration')
    def registration():
        form_reg = RegistrationForm()
        title = "Регистрация"
        return render_template('registration.html', page_title=title, form=form_reg)


    return app
