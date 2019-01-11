import os

from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow

print("PRZED IMPORTAMI API I DB MAIN INIT")

from .api import user_api
from .api import diet_api
from .database import db

print("ODPALAM MAIN/__INIT__", db)

def create_app():

    print("MAM BAZE",db)
    basedir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisissecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

    app.register_blueprint(user_api)
    app.register_blueprint(diet_api)
    app.app_context().push()

    db.init_app(app)
    CORS(app)
    return app