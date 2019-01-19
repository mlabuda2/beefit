from flask import Flask, request, jsonify, make_response, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import os

from ..database import db
from ..model.models import User, Training, TrainingPlan, TrainingPlanUser, TrainingTrainingPlan
from .user_api import token_required
from . import training_api


"""Get all trainings"""
@training_api.route('/trainings', methods=['GET'])
@token_required
def get_all_trainings(current_user):
    trainings = Training.query.all()
    output = []

    for item in trainings:
        item_data = {}
        item_data['id'] = item.id
        item_data['name'] = item.name
        item_data['body_part'] = item.body_part

        output.append(item_data)

    return jsonify({'trainings': output})


"""Get one training by id"""
@training_api.route('/training/<id>', methods=['GET'])
@token_required
def get_one_item(id):
    training = Training.query.filter_by(id=id).first()

    if not training:
        return jsonify({'message': 'No training found!'})
        
    training_data = {}
    training_data['id'] = training.id
    training_data['name'] = training.name
    training_data['body_part'] = training.body_part

    return jsonify({'training': training_data})



"""Create or delete training"""
@training_api.route('/training', methods=['POST', 'DELETE'])
@token_required
def training(current_user):
    data = request.get_json()
    if not data:
        return make_response(jsonify({'message': 'Bad Request'}), 400)
    if request.method == 'POST':
        new_training = Training(name=data['name'], body_part=data['body_part'])
        print(new_training)
        db.session.add(new_training)
        db.session.commit()

        return jsonify({'message': 'New training added!',
                        'id': new_training.id})
    elif request.method == 'DELETE':
        if current_user.admin:    
            training = Training.query.filter_by(id=data['id']).first()
            if not training:
                return make_response(jsonify({'message': 'training not exist!'}), 404)
            db.session.delete(training)
            db.session.commit()

            return jsonify({'message': 'training deleted!'})
        else:
            return jsonify({'message': 'Cannot perform that function! Admin needed!'})


"""Get user's training plans"""
@training_api.route('/user_train_plans', methods=['GET'])
@token_required
def get_user_plan(current_user):
    output = []

    user_plans = (db.session.query(TrainingPlan,TrainingPlanUser.user_id, TrainingPlanUser.training_plan_id)
        .filter(current_user.id == TrainingPlanUser.user_id)
        .filter(TrainingPlanUser.training_plan_id == TrainingPlan.id)
        .all())

    # print("MY PLANS: ",user_plans)

    for el in user_plans:
        data = {}
        data['username'] = current_user.username
        data['name'] = el.TrainingPlan.name
        data['id_plan'] = el.TrainingPlan.id

        training_plan_items = (db.session.query(TrainingTrainingPlan,Training)
            .filter(TrainingTrainingPlan.training_plan_id == el.TrainingPlan.id)
            .filter(TrainingTrainingPlan.food_item_id == Training.id)
            .all())

        #TODO
        # data["plan_details"] = []
        # all_days = dict()
        # for item in training_plan_items:
        #     # print("ITEM: ", item)

        #     weekday = item.DietPlanFoodItem.weekday # 0  0
        #     hour = item.DietPlanFoodItem.meal_time #  8  16

        #     if not all_days.get(weekday, ''):
        #         all_days[weekday] = dict() #{ 0: {} }
        #     if not all_days[weekday].get(hour, ''):
        #         all_days[weekday][hour] = []

        #     all_days[weekday][hour].append({"name": item.FoodItem.name,
        #                                     "weight": item.DietPlanFoodItem.food_item_weight,
        #                                     "pieces": item.DietPlanFoodItem.food_item_pieces
        #                                     })
        #     print("ALL: ", all_days)

        # data["plan_details"].append(all_days)
        # # print("DODAJĘ ALL DO plan_details ")
        # output.append(data)

    return jsonify({'my_diet_plans': output})