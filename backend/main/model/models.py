from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, Float, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
from flask_marshmallow import Marshmallow
import os

print("MODELS PRZED IMPORT")
from . import db

print("MODELS:", db)

class User(db.Model):
    __tablename__ = "user"
    """ Create user table"""
    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True)
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(80))
    admin = Column(Boolean)
    stature = Column(Integer()) #wzrost cm
    current_weight = Column(Integer()) #obecna waga kg
    target_weight = Column(Integer()) #docelowa waga kg
    current_calorie_intake = Column(Integer()) #obecne spożycie kcal
    diet_calorie_intake = Column(Integer()) #docelowe spożycie kcal
    bicek = Column(Integer())  # w cm 
    klata = Column(Integer())  # w cm

    def __repr__(self):
        return '<User:{}>'.format(self.username)


class DietPlanUser(db.Model):
    __tablename__ = "diet_plan_user"
    """ Create many to many relationship User<->DietPlan table"""
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    diet_plan_id = Column(Integer, ForeignKey('diet_plan.id'))

    def __repr__(self):
        return '<DietPlanUser:User_id {} has {} diet_plan_id>'.format(self.user_id, self.diet_plan_id)

class DietPlan(db.Model):
    __tablename__ = "diet_plan"
    """ Create DietPlan table"""
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __repr__(self):
        return '<DietPlan:{}>'.format(self.name)

class TrainingPlanUser(db.Model):
    __tablename__ = "training_plan_user"
    """ Create many to many relationship User<->TrainingPlan table"""
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    training_plan_id = Column(Integer, ForeignKey('training_plan.id'))

    def __repr__(self):
        return '<DietPlanUser:User_id {} has {} training_plan_id>'.format(self.user_id, self.diet_plan_id)

class TrainingPlan(db.Model):
    __tablename__ = "training_plan"
    """ Create TrainingPlan table"""
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    type = Column(String) #fbw / split itp

    def __repr__(self):
        return '<TrainingPlan:{}>'.format(self.name)

class TrainingTrainingPlan(db.Model):
    __tablename__ = "training_training_plan"
    """ Create many to many relationship Training<->Training table"""
    id = Column(Integer, primary_key=True)
    training_id = Column(Integer, ForeignKey('training.id'))
    training_plan_id = Column(Integer, ForeignKey('training_plan.id'))
    training_series = Column(Integer)
    training_repeats = Column(Integer)
    breaks_series = Column(Integer) #przerwa w sekundach między seriami
    breaks_trainings = Column(Integer) #przerwa w sekundach między ćwiczeniami
    weekday = Column(Integer) # jeśli plan jest więcej niż 1 dniowy

# tabela z ćwiczeniami
class Training(db.Model):
    __tablename__ = "training"
    """ Create Training table"""
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True)
    body_part = Column(String)

    def __repr__(self):
        return '<Training:{}>'.format(self.name)

class DietPlanFoodItem(db.Model):
    __tablename__ = "diet_plan_food_item"
    """ Create many to many relationship FoodItem<->DietPlan table"""
    id = Column(Integer, primary_key=True)
    food_item_id = Column(Integer, ForeignKey('food_item.id'))
    diet_plan_id = Column(Integer, ForeignKey('diet_plan.id'))

    meal_time = Column(Integer) #kiedy_zjeść(godzina)
    weekday = Column(Integer) # kiedy_zjeść(dzien tygodnia) 0-6 pon - niedziela
    food_item_weight = Column(Integer) #ile_zjeść (waga)
    food_item_pieces = Column(Float) #ile_zjeść (sztuki)

    def __repr__(self):
        return '<DietPlanFoodItem:DietPlan_id {} has {} food_item_id>'.format(self.diet_plan_id, self.food_item_id)


class FoodItem(db.Model):
    __tablename__ = "food_item"
    """ Create FoodItem table"""
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True)
    calories = Column(Integer)
    protein = Column(Float)
    fat = Column(Float)
    carbs = Column(Float)
    
    def __repr__(self):
        return '<FoodItem:{}>'.format(self.name)


class FoodBlacklist(db.Model):
    __tablename__ = "food_black_list"
    """ Create FoodBlacklist table"""
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    # user_id = Column(Integer, ForeignKey('user.id'))
    # total_calories = Column(Integer)

    def __repr__(self):
        return '<DietPlan:{}>'.format(self.name)