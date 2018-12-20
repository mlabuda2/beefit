from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, Float, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
from flask_marshmallow import Marshmallow
import os

db = SQLAlchemy()
ma = Marshmallow()

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


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('public_id', 'username', 'email', 'password', 'admin')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


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

class FoodItemSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name', 'calories', 'protein', 'fat', 'carbs')


fooditem_schema = FoodItemSchema()
fooditems_schema = FoodItemSchema(many=True)

class FoodBlacklist(db.Model):
    __tablename__ = "food_black_list"
    """ Create FoodBlacklist table"""
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    # user_id = Column(Integer, ForeignKey('user.id'))
    # total_calories = Column(Integer)

    def __repr__(self):
        return '<DietPlan:{}>'.format(self.name)