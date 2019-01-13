from main.model.models import User, FoodItem, DietPlan, DietPlanUser, DietPlanFoodItem
from werkzeug.security import generate_password_hash, check_password_hash

from main.database import db
from main import create_app
import csv
import sqlalchemy


print("CREATE DB:", db)
app = create_app()
db.drop_all()
db.create_all('dev')
mati = User(
    id = 0,
    public_id = "0",
    username = "mati",
    email = "mati@mati.pl",
    password = generate_password_hash("mati", method='sha256'),
    admin = True,
    stature = 180,
    current_weight = 80,
    target_weight = 100,
    current_calorie_intake = 2200,
    diet_calorie_intake = 3500,
    bicek = 40,
    klata = 130,
    )
    
wojtek = User(
    id = 1,
    public_id = "1",
    username = "wojtek",
    email = "wojtek@wojtek.pl",
    password = generate_password_hash("wojtek", method='sha256'),
    admin = True,
    stature = 180,
    current_weight = 80,
    target_weight = 100,
    current_calorie_intake = 2200,
    diet_calorie_intake = 3500,
    bicek = 40,
    klata = 130,
    )


item1 = FoodItem(
    id = 0,
    name = "kurczakTESTOWY",
    calories = 200,
    protein = 10,
    fat = 1,
    carbs = 10
)

item2 = FoodItem(
    id = 1,
    name = "tuńczykTESTOWY",
    calories = 150,
    protein = 30,
    fat = 1,
    carbs = 20
)

plan = DietPlan(
    id = 0,
    name = "PLAN DZIKA"
)

plan2 = DietPlan(
    id = 1,
    name = "PLAN KOZAKA"
)

dietPlanFoodItem1 = DietPlanFoodItem(
    diet_plan_id = 0,
    food_item_id = 0,
    meal_time = 12,
    weekday = 2,
    food_item_weight = 200,
    food_item_pieces = 0.5
)

dietPlanFoodItem2 = DietPlanFoodItem(
    diet_plan_id = 1,
    food_item_id = 1,
    meal_time = 8,
    weekday = 0,
    food_item_weight = 100,
    food_item_pieces = 2
)

dietPlanFoodItem4 = DietPlanFoodItem(
    diet_plan_id = 1,
    food_item_id = 1,
    meal_time = 16,
    weekday = 0,
    food_item_weight = 350,
    food_item_pieces = 5
)

dietPlanFoodItem5 = DietPlanFoodItem(
    diet_plan_id = 1,
    food_item_id = 1,
    meal_time = 16,
    weekday = 0,
    food_item_weight = 300,
    food_item_pieces = 20
)

dietPlanFoodItem5 = DietPlanFoodItem(
    diet_plan_id = 1,
    food_item_id = 0,
    meal_time = 16,
    weekday = 0,
    food_item_weight = 1100,
    food_item_pieces = 1
)

dietPlanFoodItem3 = DietPlanFoodItem(
    diet_plan_id = 1,
    food_item_id = 1,
    meal_time = 10,
    weekday = 1,
    food_item_weight = 300,
    food_item_pieces = 4
)



diet_plan_user = DietPlanUser(
    user_id = 0,
    diet_plan_id = 1
)

diet_plan_user_2 = DietPlanUser(
    user_id = 1,
    diet_plan_id = 0
)

diet_plan_user_3 = DietPlanUser(
    user_id = 1,
    diet_plan_id = 1
)

db.session.add(mati)
db.session.add(wojtek)
db.session.add(item1)
db.session.add(item2)
db.session.add(plan)
db.session.add(plan2)
db.session.add(dietPlanFoodItem1)
db.session.add(dietPlanFoodItem2)
db.session.add(dietPlanFoodItem3)
db.session.add(dietPlanFoodItem4)
db.session.add(dietPlanFoodItem5)
db.session.add(diet_plan_user)
db.session.add(diet_plan_user_2)
db.session.add(diet_plan_user_3)
db.session.commit()
print(User.query.all())
print(DietPlan.query.all())
print(DietPlanUser.query.all())
print(DietPlanFoodItem.query.all())



with open('TABELA_WARTOSCI_ODZYWCZYCH.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    print("PRODUKT KALORIE BIAŁKO TŁUSZCZE WĘGLOWODANY w 100g")
    for row in reader:
        print(row[0].replace('.', ''), row[1].replace(' kcal', ''), row[2].replace(' g', ''), row[3].replace(' g', ''), row[4].replace(' g', ''))
        try:
            item = FoodItem(
                    name = row[0].replace('.', ''),
                    calories = int(row[1].replace(' kcal', '')),
                    protein = row[2].replace(' g', ''),
                    fat = row[3].replace(' g', ''),
                    carbs = row[4].replace(' g', '')
                    )
            db.session.add(item)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            continue
db.session.close()