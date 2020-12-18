from webapp import app
from flask import render_template, flash, redirect
from webapp.forms import LoginForm
from webapp.get_translate import get_translate

user = {'username': 'Илья'}
cards = {
    'cat': 'кот',
    'dog': 'собака, пес'
    }


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    global cards
    form = LoginForm()
    if form.word_for_translate.data:
        word = form.word_for_translate.data
        if word not in cards.keys():
            cards[word]=get_translate(word)
        return render_template('index.html', title='Home', user=user, cards=cards, form=form)
    return render_template('index.html', title='Home', user=user, cards=cards, form=form)


users_names = ['vasya','bill', 'oleg']# хранит имена пользователей для отладки, в будущем проверть зарегистрировван пользователь или нет через bd


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name = form.username.data
    if user_name in users_names:
        return render_template('login.html', title='Sign In', form=form)
    else:
        users_names.append(user_name)
        return redirect('/registration')# отправляет на страницу с регистрацией если пользователь не залогин


@app.route('/registration')
def registration():
    form = LoginForm()
    return render_template('registration.html', title='Registration', form=form)
