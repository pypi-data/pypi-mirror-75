from app import app

from flask_boiler.context import Context as CTX
application = CTX.services.engine.wrap(app)
