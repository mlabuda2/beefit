from flask import Flask, request, jsonify, make_response, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import os
# from flask_marshmallow import Marshmallow
from models import db, User, FoodItem, DietPlan

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

app.app_context().push()
db.init_app(app)
CORS(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


"""Get all users"""
@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    users = User.query.all()
    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        # user_data['password'] = user.password
        user_data['admin'] = user.admin
        user_data['stature'] = user.stature
        user_data['current_weight'] = user.current_weight
        user_data['target_weight'] = user.target_weight
        user_data['current_calorie_intake'] = user.current_calorie_intake
        user_data['diet_calorie_intake'] = user.diet_calorie_intake
        user_data['bicek'] = user.bicek
        user_data['klata'] = user.klata
        user_data['diet_plan'] = user.diet_plan

        output.append(user_data)

    return jsonify({'users': output})


"""Get one user by public_id"""
@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})


"""Create user by admin"""
@app.route('/user', methods=['POST'])
# @token_required
# def create_user(current_user):
def create_user():
    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password,
                    email=data['email'], admin=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


"""Register user"""
@app.route('/register', methods=['POST'])
def new_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password,
                        email=data['email'], admin=True)

        db.session.add(new_user)
        db.session.commit()
    else:
        return jsonify({'message': 'Username already exist'})

    return jsonify({'message': 'New user registered!'})


"""Promote user to admin"""
@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'The user has been promoted!'})


"""Delete user"""
@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})


"""Login user"""
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


"""Get all food items"""
@app.route('/item', methods=['GET'])
@token_required
def get_all_items(current_user):
    items = FoodItem.query.all()
    output = []

    for item in items:
        item_data = {}
        item_data['id'] = item.id
        item_data['name'] = item.name
        item_data['calories'] = item.calories
        item_data['protein'] = item.protein
        item_data['fat'] = item.fat
        item_data['carbs'] = item.carbs

        output.append(item_data)

    return jsonify({'items': output})


"""Get one item by id"""
@app.route('/item/<id>', methods=['GET'])
# @token_required
def get_one_item(id):
    item = FoodItem.query.filter_by(id=id).first()

    if not item:
        return jsonify({'message': 'No item found!'})

    item_data = {}
    item_data['id'] = item.id
    item_data['name'] = item.name
    item_data['calories'] = item.calories
    item_data['protein'] = item.protein
    item_data['fat'] = item.fat
    item_data['carbs'] = item.carbs

    return jsonify({'user': item_data})


"""Create item"""
@app.route('/item', methods=['POST'])
# @token_required
def create_item():
    data = request.get_json()

    new_item = FoodItem(name=data['name'], calories=data['calories'],
                        protein=data['protein'], fat=data['fat'], carbs=data['carbs'])
    print(new_item)
    print(data)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'New item added!'})


"""Get user's diet plan"""
@app.route('/user_plan', methods=['GET'])
@token_required
def get_user_plan(current_user):
    output = []

    plans = DietPlan.query.filter_by(id=current_user.diet_plan).all()

    for plan in plans:
        plan_data = {}
        plan_data['id'] = plan.id
        plan_data['name'] = plan.name

        output.append(plan_data)

    return jsonify({'plans': output})

if __name__ == '__main__':
    app.run(debug=True)
