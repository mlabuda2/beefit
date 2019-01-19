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


#TODO
# """Create training plan"""
# @diet_api.route('/diet_plan', methods=['DELETE', 'PUT', 'POST'])
# @token_required
# def create_plan(current_user):
#     data = request.get_json()
#     if not data:
#         return make_response(jsonify({'message': 'Bad Request'}), 400)

#     if request.method == 'POST':
#         # jeśli user dodaje swoje itemy - najpierw wrzucam je do (jego profilu?) bazy
#         #TODO model CustomFoodItem n:1 User
#         if data.get('custom_items', ''):
#             for custom_item in data['custom_items']:
#                 new_item = FoodItem(name=custom_item['name'], calories=custom_item['calories'],
#                             protein=custom_item['protein'], fat=custom_item['fat'], carbs=custom_item['carbs'])
#             print("New item ADDED: ",new_item)
#             db.session.add(new_item)

#         # najpierw dodaję plan i przypisuję go do current_usera
#         new_plan = DietPlan(name=data['name'])
#         db.session.add(new_plan)
#         db.session.commit()
#         assign_plan = DietPlanUser(user_id=current_user.id, diet_plan_id=new_plan.id)

#         #dodawanie do planu itemów, z naszej bazy, które podał user
#         if data.get('our_items', ''):
#             for item in data['our_items']:
#                 assign_item = DietPlanFoodItem(food_item_id = item['food_item_id'],
#                                                 diet_plan_id = new_plan.id,
#                                                 meal_time = item['meal_time'],
#                                                 weekday = item['weekday'],
#                                                 food_item_weight = item['food_item_weight'],
#                                                 food_item_pieces = item.get('food_item_pieces', None)
#                                             )
#                 db.session.add(assign_item)
#                 print(assign_item)

#         print("DODAJĘ PLAN: ",new_plan)
#         db.session.add(assign_plan)
#         db.session.commit()

#         return jsonify({'message': 'New plan added!', "id_plan":new_plan.id })
#     elif request.method == 'DELETE':
#         if current_user.admin:    
#             diet_plan = DietPlan.query.filter_by(id=data['id']).first()
#             if not diet_plan:
#                 return make_response(jsonify({'message': 'Diet plan not exist!'}), 404)
#             db.session.delete(diet_plan)
#             db.session.commit()

#             return jsonify({'message': 'Diet plan deleted!'})
#         else:
#             return jsonify({'message': 'Cannot perform that function! Admin needed!'})
   
#     elif request.method == 'PUT':
#         diet_plan = DietPlan.query.filter_by(id=data['id_diet_plan']).first()
#         diet_plan_food_items = DietPlanFoodItem.query.filter_by(diet_plan_id = diet_plan.id).all()

#         # usuwam stare wszystkie itemy z planu 
#         for item in diet_plan_food_items:
#             db.session.delete(item)
#         db.session.commit

#         # dodaje nowe itemy do planu
#         if data.get('edited_items', ''):
#             for item in data['edited_items']:
#                 edited_item = DietPlanFoodItem(food_item_id = item['food_item_id'],
#                                                 diet_plan_id = diet_plan.id,
#                                                 meal_time = item['meal_time'],
#                                                 weekday = item['weekday'],
#                                                 food_item_weight = item['food_item_weight'],
#                                                 food_item_pieces = item.get('food_item_pieces', None)
#                                             )
#                 db.session.add(edited_item)
#                 print(edited_item)

#         db.session.commit()
#         return jsonify({'message': 'Plan edited!'})




"""Assign training plan to user"""
@training_api.route('/assign_training_plan', methods=['POST'])
@token_required
def assign_plan(current_user):
    data = request.get_json()
    if not data:
        return make_response(jsonify({'message': 'Bad Request'}), 400)
    assign_plan = TrainingPlanUser(user_id=data['user_id'], training_plan_id=data['training_plan_id'])

    print(assign_plan)
    db.session.add(assign_plan)
    db.session.commit()

    return jsonify({'message': 'Training plan assigned!'})

"""Detach training plan from user"""
@training_api.route('/detach_train_plan', methods=['POST'])
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
def assign_item(current_user):
    data = request.get_json()

    if data.get('trainings', ''):
        for item in data['trainings']:
            assign_item = TrainingTrainingPlan(training_id = item['training_id'],
                                               training_plan_id = item['training_plan_id'],
                                               training_series = item['training_series'],
                                               training_repeats = item['training_repeats'],
                                               breaks_series = item['breaks_series'], #przerwa w sekundach między seriami
                                               breaks_trainings = item['breaks_trainings'], #przerwa w sekundach między ćwiczeniami
                                               interval = item['interval'], # 1-dniowy/ 2-dniowy itp
                                        )
            db.session.add(assign_item)
            print(assign_item)

    print("PRZYPISUJĘ TRENINGI(ĆWICZENIA) DO PLANU")
    db.session.commit()

    return jsonify({'message': 'Trainings assigned!'})


#TODO
# """Get all training plans"""
# @training_api.route('/all_plans', methods=['GET'])
# @token_required
# def get_all_plans(current_user):
#     output = []

#     plans = db.session.query(DietPlan).all()
#     print("MY PLANS: ", plans)

#     for plan in plans:
#         data = {}
#         data['name'] = plan.name
#         data['id_plan'] = plan.id

#         diet_plan_items = (db.session.query(DietPlanFoodItem,FoodItem)
#             .filter(DietPlanFoodItem.diet_plan_id == plan.id)
#             .filter(DietPlanFoodItem.food_item_id == FoodItem.id)
#             .all())

#         data["plan_details"] = []
#         all_days = dict()
#         for item in diet_plan_items:
#             print("ITEM: ", item)

#             weekday = item.DietPlanFoodItem.weekday # 0  0
#             hour = item.DietPlanFoodItem.meal_time #  8  16

#             if not all_days.get(weekday, ''):
#                 all_days[weekday] = dict() #{ 0: {} }
#             if not all_days[weekday].get(hour, ''):
#                 all_days[weekday][hour] = []

#             all_days[weekday][hour].append({"name": item.FoodItem.name,
#                                             "weight": item.DietPlanFoodItem.food_item_weight,
#                                             "pieces": item.DietPlanFoodItem.food_item_pieces
#                                             })
#             print("ALL: ", all_days)

#         data["plan_details"].append(all_days)
#         print("DODAJĘ ALL DO plan_details ")
#         output.append(data)

#     return jsonify({'diet_plans': output})

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

    training_plan_items = (db.session.query(TrainingTrainingPlan,Training)
        .filter(TrainingTrainingPlan.training_plan_id == plan.id)
        .filter(TrainingTrainingPlan.training_item_id == Training.id)
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

    return jsonify({'my_training_plans': output})