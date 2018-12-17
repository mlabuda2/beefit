from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    __tablename__ = "users"
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    stature = db.Column(db.Integer()) #wzrost cm
    current_weight = db.Column(db.Integer()) #obecna waga kg
    target_weight = db.Column(db.Integer()) #docelowa waga kg
    current_calorie_intake = db.Column(db.Integer()) #obecne spożycie kcal
    diet_calorie_intake = db.Column(db.Integer()) #docelowe spożycie kcal
    bicek = db.Column(db.String())  # w cm 
    klata = db.Column(db.String())  # w cm

    def __init__(self, public_id, username, password, email, admin):
        self.public_id = public_id
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin
        if username == "matjas":
            self.bicek = "100" #cm
            self.klata = "200" #cm
            self.weight = "150" #kg

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