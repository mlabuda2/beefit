from api import db
from models import User, FoodItem, DietPlan, DietPlanUser
from werkzeug.security import generate_password_hash, check_password_hash

db.drop_all()
db.create_all()
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

plan = DietPlan(
    id = 0,
    name = "PLAN DZIKA"
)

plan2 = DietPlan(
    id = 1,
    name = "PLAN KOZAKA"
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
db.session.add(plan)
db.session.add(plan2)
db.session.add(diet_plan_user)
db.session.add(diet_plan_user_2)
db.session.add(diet_plan_user_3)
db.session.commit()
print(User.query.all())
print(DietPlan.query.all())
print(DietPlanUser.query.all())