from flask import Flask
from view import TodoMediator


TodoMediator.start()

app = Flask(__name__)


@app.route('/', methods=('GET',))
def hello():
    return 'world'

