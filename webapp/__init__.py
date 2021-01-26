from flask import Flask, request, redirect, render_template, flash, url_for
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

    @app.route('/my_dictionary')
    def my_dictionary():
        title = "Мой словарь"
        cards_db = Cards.query.filter(Cards.user_id==current_user.get_id()).all()
        word_form = WordForm()
        if current_user.is_authenticated:
            return render_template('my_dictionary.html', page_title=title, cards=cards_db, form=word_form)
        else:
            flash('вы не вошли на сайт')
            return redirect(url_for('login'))

    @app.route('/add_word', methods=["POST"])
    def add_word():
        form = WordForm()
        user_id = current_user.get_id()
        if form.add.data:
            word_exist_in_db = Cards.query.filter(Cards.original_word==form.word_for_translate.data, Cards.user_id==user_id).count()
            if not word_exist_in_db:
                if form.validate_on_submit():
                    translation = get_translation(form.word_for_translate.data)
                    if translation:
                        new_word = Cards(original_word=form.word_for_translate.data, translatted_word=translation, user_id=user_id)
                        db.session.add(new_word)
                        db.session.commit()
                        flash('Вы успешно добавили слово!')
                    else:
                        flash('Не найден перевод')
            else:
                flash('Слово уже в вашем словаре')
            return redirect(url_for('my_dictionary'))
        else:
            translation = get_translation(form.word_for_translate.data)
            if translation:
                trnlated_word = translation
                flash(form.word_for_translate.data)
                flash(trnlated_word)
            else:
                flash('Не найден перевод')
            return redirect(url_for('my_dictionary'))

    @app.route('/word_edit/<int:word_id>', methods=['POST', 'GET'])
    def word_edit(word_id):
        word = Cards.query.filter(Cards.id==word_id).first()
        form = WordForm()
        if request.method == 'GET':
            return render_template('word_edit.html', form=form, cards=word)
        else:
            if form.validate_on_submit():
                word.original_word = form.word_for_translate.data 
                word.translatted_word = form.transleted_word.data
                db.session.commit()
                return redirect(url_for('my_dictionary'))

            else:
                return redirect(url_for('my_dictionary'))

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
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        else:
            form_reg = RegistrationForm()
            title = "Регистрация"
            return render_template('registration.html', page_title=title, form=form_reg)

    @app.route('/process_reg', methods=['POST'])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data, email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались!')
            return redirect(url_for('index'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле {}: - {}'.format(
                        getattr(form, field).label.text,
                        error
                    ))
            return redirect(url_for('registration'))

    return app
