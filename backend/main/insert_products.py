import csv
import sqlalchemy
from api import db
from models import User, FoodItem, DietPlan, DietPlanUser, DietPlanFoodItem


db.drop_all()
db.create_all()

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