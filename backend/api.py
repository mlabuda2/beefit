from flask import Flask, request, jsonify, make_response, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = "users"
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def __init__(self, public_id, username, password, email, admin):
        self.public_id = public_id
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('public_id', 'username', 'email', 'password', 'admin')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class FoodItem(db.Model):
    __tablename__ = "food_items"
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    calories = db.Column(db.Integer)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carbs = db.Column(db.Float)

    def __init__(self, name, calories, protein, fat, carbs):
        self.name = name
        self.calories = calories
        self.protein = protein
        self.fat = fat
        self.carbs = carbs


class FoodItemSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name', 'calories', 'protein', 'fat', 'carbs')


fooditem_schema = FoodItemSchema()
fooditems_schema = FoodItemSchema(many=True)


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
        user_data['password'] = user.password
        user_data['admin'] = user.admin
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
                        email=data['email'], admin=False)

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
# @token_required
def get_all_items():
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


if __name__ == '__main__':
    app.run(debug=True)
