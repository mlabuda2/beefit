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
from ..model.models import User, FoodItem, DietPlan, DietPlanUser, DietPlanFoodItem
from .user_api import token_required
from . import diet_api


"""Get all food items"""
@diet_api.route('/items', methods=['GET'])
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
@diet_api.route('/item/<id>', methods=['GET'])
@token_required
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

    return jsonify({'item': item_data})


"""Create or delete item"""
@diet_api.route('/item', methods=['POST', 'DELETE'])
@token_required
def item(current_user):
    data = request.get_json()
    if not data:
        return make_response(jsonify({'message': 'Bad Request'}), 400)
    if request.method == 'POST':
        new_item = FoodItem(name=data['name'], calories=data['calories'],
                            protein=data['protein'], fat=data['fat'], carbs=data['carbs'])
        print(new_item)
        db.session.add(new_item)
        db.session.commit()

        return jsonify({'message': 'New item added!',
                        'id': new_item.id})
    elif request.method == 'DELETE':
        if current_user.admin:    
            item = FoodItem.query.filter_by(id=data['id']).first()
            if not item:
                return make_response(jsonify({'message': 'Item not exist!'}), 404)
            db.session.delete(item)
            db.session.commit()

            return jsonify({'message': 'Item deleted!'})
        else:
            return jsonify({'message': 'Cannot perform that function! Admin needed!'})

"""Get user's diet plans"""
@diet_api.route('/user_plans', methods=['GET'])
@token_required
def get_user_plan(current_user):
    output = []

    user_plans = (db.session.query(DietPlan,DietPlanUser.user_id, DietPlanUser.diet_plan_id)
        .filter(current_user.id == DietPlanUser.user_id)
        .filter(DietPlanUser.diet_plan_id == DietPlan.id)
        .all())

    # print("MY PLANS: ",user_plans)

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
            # print("ITEM: ", item)

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
            print("ALL: ", all_days)

        data["plan_details"].append(all_days)
        # print("DODAJĘ ALL DO plan_details ")
        output.append(data)

    return jsonify({'my_diet_plans': output})

"""Create diet plan"""
@diet_api.route('/diet_plan', methods=['DELETE', 'PUT', 'POST'])
@token_required
def create_plan(current_user):
    data = request.get_json()
    if not data:
        return make_response(jsonify({'message': 'Bad Request'}), 400)

    if request.method == 'POST':
        # jeśli user dodaje swoje itemy - najpierw wrzucam je do (jego profilu?) bazy
        #TODO model CustomFoodItem n:1 User
        if data.get('custom_items', ''):
            for custom_item in data['custom_items']:
                new_item = FoodItem(name=custom_item['name'], calories=custom_item['calories'],
                            protein=custom_item['protein'], fat=custom_item['fat'], carbs=custom_item['carbs'])
            print("New item ADDED: ",new_item)
            db.session.add(new_item)

        # najpierw dodaję plan i przypisuję go do current_usera
        new_plan = DietPlan(name=data['name'])
        db.session.add(new_plan)
        db.session.commit()
        assign_plan = DietPlanUser(user_id=current_user.id, diet_plan_id=new_plan.id)

        #dodawanie do planu itemów, z naszej bazy, które podał user
        if data.get('our_items', ''):
            for item in data['our_items']:
                assign_item = DietPlanFoodItem(food_item_id = item['food_item_id'],
                                                diet_plan_id = new_plan.id,
                                                meal_time = item['meal_time'],
                                                weekday = item['weekday'],
                                                food_item_weight = item['food_item_weight'],
                                                food_item_pieces = item.get('food_item_pieces', None)
                                            )
                db.session.add(assign_item)
                print(assign_item)

        print("DODAJĘ PLAN: ",new_plan)
        db.session.add(assign_plan)
        db.session.commit()

        return jsonify({'message': 'New plan added!', "id_plan":new_plan.id })
    elif request.method == 'DELETE':
        if current_user.admin:    
            diet_plan = DietPlan.query.filter_by(id=data['id']).first()
            if not diet_plan:
                return make_response(jsonify({'message': 'Diet plan not exist!'}), 404)
            db.session.delete(diet_plan)
            db.session.commit()

            return jsonify({'message': 'Diet plan deleted!'})
        else:
            return jsonify({'message': 'Cannot perform that function! Admin needed!'})
   
    elif request.method == 'PUT':
        diet_plan = DietPlan.query.filter_by(id=data['id_diet_plan']).first()
        diet_plan_food_items = DietPlanFoodItem.query.filter_by(diet_plan_id = diet_plan.id).all()

        # usuwam stare wszystkie itemy z planu 
        for item in diet_plan_food_items:
            db.session.delete(item)
        db.session.commit

        # dodaje nowe itemy do planu
        if data.get('edited_items', ''):
            for item in data['edited_items']:
                edited_item = DietPlanFoodItem(food_item_id = item['food_item_id'],
                                                diet_plan_id = diet_plan.id,
                                                meal_time = item['meal_time'],
                                                weekday = item['weekday'],
                                                food_item_weight = item['food_item_weight'],
                                                food_item_pieces = item.get('food_item_pieces', None)
                                            )
                db.session.add(edited_item)
                print(edited_item)

        db.session.commit()
        return jsonify({'message': 'Plan edited!'})


"""Assign diet plan to user"""
@diet_api.route('/assign_plan', methods=['POST'])
@token_required
def assign_plan(current_user):
    data = request.get_json()
    if not data:
        return make_response(jsonify({'message': 'Bad Request'}), 400)
    assign_plan = DietPlanUser(user_id=current_user.id, diet_plan_id=data['diet_plan_id'])

    print(assign_plan)
    db.session.add(assign_plan)
    db.session.commit()

    return jsonify({'message': 'Plan assigned!'})

"""Detach diet plan from user"""
@diet_api.route('/detach_plan', methods=['POST'])
@token_required
def detach_plan(current_user):
    data = request.get_json()
    if not data:
        return make_response(jsonify({'message': 'Bad Request'}), 400)
    detached_plan = (db.session.query(DietPlanUser)
                    .filter(DietPlanUser.user_id==current_user.id)
                    .filter(DietPlanUser.diet_plan_id==data['diet_plan_id'])).first()
    print(detached_plan)

    db.session.delete(detached_plan)
    db.session.commit()

    return jsonify({'message': 'Plan detached!'})


"""Assign food_item/items to diet plan"""
@diet_api.route('/assign_items', methods=['POST'])
@token_required
def assign_item(current_user):
    data = request.get_json()

    if data.get('items', ''):
        for item in data['items']:
            assign_item = DietPlanFoodItem(food_item_id = item['food_item_id'],
                                            diet_plan_id = item['diet_item_id'],
                                            meal_time = item['meal_time'],
                                            weekday = item['weekday'],
                                            food_item_weight = item['food_item_weight'],
                                            food_item_pieces = item.get('food_item_pieces', None)
                                        )
            db.session.add(assign_item)
            print(assign_item)

    print("PRZYPISUJĘ ITEMKI DO PLANU")
    db.session.commit()


    return jsonify({'message': 'Item assigned!'})



"""Get all diet plans"""
@diet_api.route('/all_plans', methods=['GET'])
@token_required
def get_all_plans(current_user):
    output = []

    plans = db.session.query(DietPlan).all()
    print("MY PLANS: ", plans)

    for plan in plans:
        data = {}
        data['name'] = plan.name
        data['id_plan'] = plan.id

        diet_plan_items = (db.session.query(DietPlanFoodItem,FoodItem)
            .filter(DietPlanFoodItem.diet_plan_id == plan.id)
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
            print("ALL: ", all_days)

        data["plan_details"].append(all_days)
        print("DODAJĘ ALL DO plan_details ")
        output.append(data)

    return jsonify({'diet_plans': output})

"""Get user's diet plan by id"""
@diet_api.route('/plan/<id>', methods=['GET'])
@token_required
def get_plan_by_id(current_user, id):
    output = []

    plan = (db.session.query(DietPlan)
        .filter(DietPlan.id == id)
        .first())

    print("PLAN BY ID: ",plan)

    data = {}
    data['username'] = current_user.username
    data['name'] = plan.name
    data['id_plan'] = plan.id

    diet_plan_items = (db.session.query(DietPlanFoodItem,FoodItem)
        .filter(DietPlanFoodItem.diet_plan_id == plan.id)
        .filter(DietPlanFoodItem.food_item_id == FoodItem.id)
        .all())

    data["plan_details"] = []
    all_days = dict()
    for item in diet_plan_items:
        # print("ITEM: ", item)

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
        print("ALL: ", all_days)

    data["plan_details"].append(all_days)
    # print("DODAJĘ ALL DO plan_details ")
    output.append(data)

    return jsonify({'my_diet_plans': output})
