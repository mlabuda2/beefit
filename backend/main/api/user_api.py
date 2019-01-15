from flask import Blueprint, request, jsonify
from ..model.models import db, User
from flask import Flask, request, jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import os
from flask import current_app as app
from . import user_api


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY']) #TODO
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
@user_api.route('/is_auth', methods=['GET'])
@token_required
def is_authenticated(current_user):
    return jsonify({'message': 'OK'})


"""Get all users"""
@user_api.route('/user', methods=['GET'])
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
@user_api.route('/user/<public_id>', methods=['GET'])
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
@user_api.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password,
                    email=data['email'], admin=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


"""Register user"""
@user_api.route('/register', methods=['POST'])
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
@user_api.route('/user/<public_id>', methods=['PUT'])
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
@user_api.route('/user/<public_id>', methods=['DELETE'])
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
@user_api.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="User not found!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode( #TODO
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)},
            app.config['SECRET_KEY'])
        # token = jwt.encode(
        #     {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)},
        #     'thisissecret')

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
