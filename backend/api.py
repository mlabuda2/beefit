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
from models import db, User, FoodItem, DietPlan, DietPlanUser, DietPlanFoodItem

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
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except:    
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# """Refresh token"""
# @app.route('/refresh', methods=['GET'])
# @token_required
# def is_authenticated(current_user):
#     return jsonify({'message': 'OK'})


"""Is authenticated"""
@app.route('/is_auth', methods=['GET'])
@token_required
def is_authenticated(current_user):
    return jsonify({'message': 'OK'})


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
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="User not found!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
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


"""Get user's diet plans"""
@app.route('/user_plan', methods=['GET'])
@token_required
def get_user_plan(current_user):
    output = []


    user_plans = (db.session.query(DietPlan,DietPlanUser.user_id, DietPlanUser.diet_plan_id)
        .filter(current_user.id == DietPlanUser.user_id)
        .filter(DietPlanUser.diet_plan_id == DietPlan.id)
        .all())

    print("MY PLANS: ",user_plans)

    for el in user_plans:
        data = {}
        data['username'] = current_user.username
        data['name'] = el.DietPlan.name
        data['id_plan'] = el.DietPlan.id

        diet_plan_items = (db.session.query(DietPlanFoodItem,FoodItem)
            .filter(DietPlanFoodItem.diet_plan_id == el.DietPlan.id)
            .filter(DietPlanFoodItem.food_item_id == FoodItem.id)
            .all())

        data["plan_details"] = []
        all_days = dict()
        for item in diet_plan_items:
            print("ITEM: ", item)

            weekday = item.DietPlanFoodItem.weekday # 0  0 
            hour = item.DietPlanFoodItem.meal_time #  8  16

            if not all_days.get(weekday, ''):
                all_days[weekday] = dict() #{ 0: {} }
            if not all_days[weekday].get(hour, ''):
                all_days[weekday][hour] = []

            all_days[weekday][hour].append({"name": item.FoodItem.name,
                                            "weight": item.DietPlanFoodItem.food_item_weight,
                                            "pieces": item.DietPlanFoodItem.food_item_pieces
                                            })
            # all_days[weekday][hour].append(item.DietPlanFoodItem.food_item_weight)
            # all_days[weekday][hour].append(item.DietPlanFoodItem.food_item_pieces)
            print("ALL: ", all_days)

        data["plan_details"].append(all_days)
        print("DODAJĘ ALL DO plan_details ")
        output.append(data)

    return jsonify({'my_diet_plans': output})

if __name__ == '__main__':
    app.run(debug=True)
