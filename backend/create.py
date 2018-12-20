from api import db
from models import User, FoodItem, DietPlan
from werkzeug.security import generate_password_hash, check_password_hash

db.drop_all()
db.create_all()
mati = User(public_id = "0",
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
    diet_plan = 1
    )

plan = DietPlan(
    id = 1
)

db.session.add(mati)
db.session.add(plan)
db.session.commit()
print(User.query.all())
print(DietPlan.query.all())