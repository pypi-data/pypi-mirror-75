from flask import Flask
from view import TodoMediator


TodoMediator.start()

app = Flask(__name__)

from flask_boiler.context import Context as CTX
application = CTX.services.engine.wrap(app)


@app.route('/', methods=('GET',))
def hello():
    return 'world'

