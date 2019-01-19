from flask import Blueprint

print("ODPALAM API/__INIT__")
user_api = Blueprint('user_api', __name__)
diet_api = Blueprint('diet_api', __name__)
training_api = Blueprint('training_api', __name__)