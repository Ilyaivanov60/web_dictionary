from flask import Flask

cards = [
    {'cat' : 'кот'},
    {'dog' : 'собака, пес'},
    {'car' : 'автомобиль, машина'},
    {'bag' : 'сумка, мешок'},
    {'bed' : 'кровать, постель}'},
    {'box' : 'коробка, ящик'},
    {'bottle ' : 'бутылка'},
    {'bank' : 'банк'},
    {'book ' : 'книга'}
    ]

app = Flask(__name__)

@app.route('/')
def index():
    return str(cards)

if __name__ == '__main__':
    app.run()