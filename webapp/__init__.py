from flask import Flask
from webapp.config import SECRET_KEY


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


from webapp import routes
