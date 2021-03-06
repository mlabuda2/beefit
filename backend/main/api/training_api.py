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

            return jsonify({'message': 'Training deleted!'})
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
        data['type'] = el.TrainingPlan.type

        training_plan_items = (db.session.query(TrainingTrainingPlan,Training)
            .filter(TrainingTrainingPlan.training_plan_id == el.TrainingPlan.id)
            .filter(TrainingTrainingPlan.training_id == Training.id)
            .all())

        data["plan_details"] = []
        all_days = dict()
        for item in training_plan_items:
            # print("ITEM: ", item)

            weekday = item.TrainingTrainingPlan.weekday # 3

            if not all_days.get(weekday, ''):
                all_days[weekday] = [] #{ 3: {} }

            all_days[weekday].append({"name": item.Training.name,
                                      "body_part": item.Training.body_part,
                                      "training_series": item.TrainingTrainingPlan.training_series,
                                      "training_repeats": item.TrainingTrainingPlan.training_repeats,
                                      "breaks_series": item.TrainingTrainingPlan.breaks_series,
                                      "breaks_trainings": item.TrainingTrainingPlan.breaks_trainings,
                                     })
            print("ALL: ", all_days)

        data["plan_details"].append(all_days)
        output.append(data)

    return jsonify({'my_training_plans': output})


"""Create/delete/edit training plan"""
@training_api.route('/training_plan', methods=['DELETE', 'PUT', 'POST'])
@token_required
def create_plan(current_user):
    data = request.get_json()
    if not data:
        return make_response(jsonify({'message': 'Bad Request'}), 400)

    if request.method == 'POST':
    #     # jeśli user dodaje swoje itemy - najpierw wrzucam je do (jego profilu?) bazy
    #     #TODO model CustomFoodItem n:1 User
    #     if data.get('custom_items', ''):
    #         for custom_item in data['custom_items']:
    #             new_item = FoodItem(name=custom_item['name'], calories=custom_item['calories'],
    #                         protein=custom_item['protein'], fat=custom_item['fat'], carbs=custom_item['carbs'])
    #         print("New item ADDED: ",new_item)
    #         db.session.add(new_item)

        # najpierw dodaję plan i przypisuję go do current_usera
        new_plan = TrainingPlan(name=data['name'], type=data['type'])
        db.session.add(new_plan)
        db.session.commit()
        assign_plan = TrainingPlanUser(user_id=current_user.id, training_plan_id=new_plan.id)

        #dodawanie do planu itemów, z naszej bazy, które podał user
        if data.get('our_trainings', ''):
            for item in data['our_trainings']:
                assign_item = TrainingTrainingPlan(training_id = item['training_id'],
                                                   training_plan_id = new_plan.id,
                                                   training_series = item['training_series'],
                                                   training_repeats = item['training_repeats'],
                                                   breaks_series = item['breaks_series'], #przerwa w sekundach między seriami
                                                   breaks_trainings = item['breaks_trainings'], #przerwa w sekundach między ćwiczeniami
                                                   weekday = item['weekday'], # 1-dniowy/ 2-dniowy itp
                                                  )
                db.session.add(assign_item)
                print(assign_item)

        print("DODAJĘ PLAN: ",new_plan)
        db.session.add(assign_plan)
        db.session.commit()

        return jsonify({'message': 'New trainig plan added!', "id_plan":new_plan.id })
    elif request.method == 'DELETE':
        if current_user.admin:    
            training_plan = TrainingPlan.query.filter_by(id=data['id']).first()
            if not training_plan:
                return make_response(jsonify({'message': 'Training plan not exist!'}), 404)
            db.session.delete(training_plan)
            db.session.commit()

            return jsonify({'message': 'Training plan deleted!'})
        else:
            return jsonify({'message': 'Cannot perform that function! Admin needed!'})
   
    elif request.method == 'PUT':
        training_plan = TrainingPlan.query.filter_by(id=data['id_training_plan']).first()
        training_train_plan = TrainingTrainingPlan.query.filter_by(training_plan_id = training_plan.id).all()

        # usuwam stare wszystkie itemy z planu 
        for item in training_train_plan:
            db.session.delete(item)
        db.session.commit

        
        #dodaje nowe ćwiczenia do planu
        if data.get('edited_trainings', ''):
            for item in data['edited_trainings']:
                edited_training = TrainingTrainingPlan(training_id = item['training_id'],
                                                       training_plan_id = training_plan.id,
                                                       training_series = item['training_series'],
                                                       training_repeats = item['training_repeats'],
                                                       breaks_series = item['breaks_series'], #przerwa w sekundach między seriami
                                                       breaks_trainings = item['breaks_trainings'], #przerwa w sekundach między ćwiczeniami
                                                       weekday = item['weekday'], # 1-dniowy/ 2-dniowy itp
                                                      )
                db.session.add(edited_training)
                print(edited_training)

        db.session.commit()
        return jsonify({'message': 'Training plan edited!'})

"""Assign training plan to user"""
@training_api.route('/assign_training_plan', methods=['POST'])
@token_required
def assign_plan(current_user):
    data = request.get_json()
    if not data:
        return make_response(jsonify({'message': 'Bad Request'}), 400)
    assign_plan = TrainingPlanUser(user_id=current_user.id, training_plan_id=data['training_plan_id'])

    print(assign_plan)
    db.session.add(assign_plan)
    db.session.commit()

    return jsonify({'message': 'Training plan assigned!'})

"""Detach training plan from user"""
@training_api.route('/detach_training_plan', methods=['POST'])
@token_required
def detach_plan(current_user):
    data = request.get_json()
    if not data:
        return make_response(jsonify({'message': 'Bad Request'}), 400)
    detached_plan = (db.session.query(TrainingPlanUser)
                    .filter(TrainingPlanUser.user_id==current_user.id)
                    .filter(TrainingPlanUser.training_plan_id==data['training_plan_id'])).first()
    print(detached_plan)

    db.session.delete(detached_plan)
    db.session.commit()

    return jsonify({'message': 'Trainig plan detached!'})


"""Assign training/trainings to diet plan"""
@training_api.route('/assign_trainings', methods=['POST'])
@token_required
def assign_training(current_user):
    data = request.get_json()

    if data.get('trainings', ''):
        for item in data['trainings']:
            assign_item = TrainingTrainingPlan(training_id = item['training_id'],
                                               training_plan_id = item['training_plan_id'],
                                               training_series = item['training_series'],
                                               training_repeats = item['training_repeats'],
                                               breaks_series = item['breaks_series'], #przerwa w sekundach między seriami
                                               breaks_trainings = item['breaks_trainings'], #przerwa w sekundach między ćwiczeniami
                                               weekday = item['weekday'], # 1-dniowy/ 2-dniowy itp
                                              )
            db.session.add(assign_item)
            print(assign_item)

    print("PRZYPISUJĘ TRENINGI(ĆWICZENIA) DO PLANU")
    db.session.commit()

    return jsonify({'message': 'Trainings assigned!'})


#TODO
"""Get all training plans"""
@training_api.route('/all_training_plans', methods=['GET'])
@token_required
def get_all_plans(current_user):
    output = []

    plans = db.session.query(TrainingPlan).all()
    print("MY PLANS: ", plans)

    for plan in plans:
        data = {}
        data['name'] = plan.name
        data['id_plan'] = plan.id
        data['type'] = plan.type

        training_plan_items = (db.session.query(TrainingTrainingPlan,Training)
            .filter(TrainingTrainingPlan.training_plan_id == plan.id)
            .filter(TrainingTrainingPlan.training_id == Training.id)
            .all())

        data["plan_details"] = []
        all_days = dict()
        for item in training_plan_items:
            weekday = item.TrainingTrainingPlan.weekday # 3

            if not all_days.get(weekday, ''):
                all_days[weekday] = [] #{ 3: {} }

            all_days[weekday].append({"name": item.Training.name,
                                      "body_part": item.Training.body_part,
                                      "training_series": item.TrainingTrainingPlan.training_series,
                                      "training_repeats": item.TrainingTrainingPlan.training_repeats,
                                      "breaks_series": item.TrainingTrainingPlan.breaks_series,
                                      "breaks_trainings": item.TrainingTrainingPlan.breaks_trainings,
                                     })
            print("ALL: ", all_days)

        data["plan_details"].append(all_days)
        output.append(data)

    return jsonify({'training_plans': output})


"""Get user's training plan by id"""
@training_api.route('/training_plan/<id>', methods=['GET'])
@token_required
def get_plan_by_id(current_user, id):
    output = []

    plan = (db.session.query(TrainingPlan)
        .filter(TrainingPlan.id == id)
        .first())

    print("PLAN BY ID: ",plan)

    data = {}
    data['username'] = current_user.username
    data['name'] = plan.name
    data['id_plan'] = plan.id
    data['type'] = plan.type

    training_plan_items = (db.session.query(TrainingTrainingPlan,Training)
        .filter(TrainingTrainingPlan.training_plan_id == plan.id)
        .filter(TrainingTrainingPlan.training_id == Training.id)
        .all())

    data["plan_details"] = []
    all_days = dict()
    for item in training_plan_items:
        weekday = item.TrainingTrainingPlan.weekday # 3

        if not all_days.get(weekday, ''):
            all_days[weekday] = [] #{ 3: {} }

        all_days[weekday].append({"name": item.Training.name,
                                  "body_part": item.Training.body_part,
                                  "training_series": item.TrainingTrainingPlan.training_series,
                                  "training_repeats": item.TrainingTrainingPlan.training_repeats,
                                  "breaks_series": item.TrainingTrainingPlan.breaks_series,
                                  "breaks_trainings": item.TrainingTrainingPlan.breaks_trainings
                                })
        print("ALL: ", all_days)

    data["plan_details"].append(all_days)
    output.append(data)

    return jsonify({'training_plan': output})