from webapp import app
from flask import render_template, flash, redirect
from webapp.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():

    user = {'username': 'Илья'}
    cards = [
        {'cat' : 'кот'},
        {'dog' : 'собака, пес'},
        {'car' : 'автомобиль, машина'},
        {'bag' : 'сумка, мешок'},
        {'bed' : 'кровать, постель}'},
        {'box' : 'коробка, ящик'},
        {'bottle' : 'бутылка'},
        {'bank' : 'банк'},
        {'book' : 'книга'}
    ]
    return render_template('index.html', title='Home', user=user, cards=cards)

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