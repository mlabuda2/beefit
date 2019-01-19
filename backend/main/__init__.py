import os

from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow

print("PRZED IMPORTAMI API I DB MAIN INIT")

from .api import user_api
from .api import diet_api
from .api import training_api
from .database import db
from .config import config_by_name

print("ODPALAM MAIN/__INIT__", db)

def create_app(config_name):
    print("MAM BAZE",db)
    basedir = os.path.abspath(os.path.dirname(__file__))

    print("STATUS: ", config_name)
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.register_blueprint(user_api)
    app.register_blueprint(diet_api)
    app.register_blueprint(training_api)
    app.app_context().push()

    db.init_app(app)
    CORS(app)
    return app