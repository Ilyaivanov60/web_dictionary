from flask import Blueprint, request, redirect, render_template, flash, url_for
from flask_login import current_user

from get_translated_word import get_translation
from webapp.db import db
from webapp.word.models import Cards
from webapp.word.forms import WordForm


blueprint = Blueprint('word', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def index():
    title = "Домашная страница"
    return render_template('word/index.html', page_title=title)

@blueprint.route('/my_dictionary')
def my_dictionary():
    title = "Мой словарь"
    cards_db = Cards.query.filter(Cards.user_id==current_user.get_id()).all()
    word_form = WordForm()
    if current_user.is_authenticated:
        return render_template('word/my_dictionary.html', page_title=title, cards=cards_db, form=word_form)
    else:
        flash('вы не вошли на сайт')
        return redirect(url_for('user.login'))

@blueprint.route('/add_word', methods=["POST"])
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
        return redirect(url_for('word.my_dictionary'))
    elif form.submit.data:
        translation = get_translation(form.word_for_translate.data)
        if translation:
            trnlated_word = translation
            flash(form.word_for_translate.data)
            flash(trnlated_word)
        else:
            flash('Не найден перевод')
        return redirect(url_for('word.my_dictionary'))

@blueprint.route('/delete_word/<int:word_id>')
def delete_word(word_id):
    user_id = current_user.get_id()
    word_to_del = Cards.query.filter(Cards.id==word_id, Cards.user_id==user_id).first()
    db.session.delete(word_to_del)
    db.session.commit()
    flash ("Вы успешно удалили слово")
    return redirect(url_for('word.my_dictionary')) 

@blueprint.route('/word_edit/<int:word_id>', methods=['POST', 'GET'])
def word_edit(word_id):
    word = Cards.query.filter(Cards.id==word_id).first()
    form = WordForm()
    if request.method == 'GET':
        return render_template('word/word_edit.html', form=form, cards=word)
    else:
        if form.validate_on_submit():
            word.original_word = form.word_for_translate.data 
            word.translatted_word = form.transleted_word.data
            db.session.commit()
            return redirect(url_for('word.my_dictionary'))

        else:
            return redirect(url_for('word.my_dictionary'))