
# DOKUMENTACJA API

##### PIERWSZE URUCHAMIANIE:
```
1. python create.py
```
#### KOLEJNE URUCHAMIANIA:
```
1.'python manage.py run'
```

## API UŻYTKOWNIKÓW

#### LOGOWANIE ADMIN
```
(postman)
Basic Auth
U: mati
P: mati
otrzymujemy token
```
#### DZIAŁANIA Z TOKENEM
```
header: 
    key: x-access-token
    value: "tutaj otrzymany token"
```
#### REJESTRACJA NOWEGO UŻYTKOWNIKA (/register):
```
metoda: POST
body: {
"username": "user1",
"email": "user1@user.pl",
"password": "user1"
}
```


## API PLANÓW DIETETYCZNYCH

#### ZWRACA PLANY ZALOGOWANEGO USERA (/user_plans): + wyjaśnienie responsea
```
headers standardowo x-access-token
metoda: GET

wyjaśnienie responsea: 

"plan_details": [
                {
                    "0": {      # tutaj 0 to dzień tygodnia
                        "8": [  # tutaj 8 to godzina posiłku
                            {
                                "name": "jabłko",
                                "pieces": 2,        # to znaczy że mają zostać zjedzone 2 jabłka czyli 
                                "weight": 400       # mniej więcej 400 gram. (!!!! NIE 2x400 !!!!!!!!)
                            }                       # weight mogłoby być NULL w tym przypadku
                        ],
                        "16": [
                            {
                                "name": "tuńczyk",
                                "pieces": 5,
                                "weight": 350
                            },
                            {
                                "name": "kurczak",
                                "pieces": 1,
                                "weight": 1100
                            }
                        ]
                    },
                    "1": {
                        "10": [
                            {
                                "name": "tuńczyk",
                                "pieces": 4,
                                "weight": 300
                            }
                        ]
                    }
                }
            ],
```

#### ZWRACA DIET PLAN BY ID (/plan/id):
```
headers standardowo x-access-token
metoda: GET
```

#### TWORZENIE, USUWANIE LUB EDYCJA DIET PLANU  (/plan):
```
headers standardowo x-access-token

DODAWANIE
metoda: POST
body: {
"name": "plan pełny",
# user podaje itemy które mamy w bazie
"our_items": [ 
                {
                    "food_item_id": 33,
                    "meal_time": 8,
                    "weekday": 0,
                    "food_item_weight": 100
                },
                {
                    "food_item_id": 34,
                    "meal_time": 12,
                    "weekday": 0,
                    "food_item_weight": 200,
                    "food_item_pieces: 1 #opcjonalnie - nie trzeba podawać
                }
            ],

#opcjonalnie - nie trzeba podawać / NIEDOKOŃCZONE narazie dodaje do tabeli głównej(FoodItem) później do CustomFoodItem usera zrobię
#user może podać itemy których nie mamy w bazie

"custom_items": [   
                {
                    "name": "item4",
                    "calories": 10,
                    "protein": 10.6, 
                    "fat": 10.3, 
                    "carbs": 10.3
                }, ...
                ]
}


USUWANIE   (tylko ADMIN)
metoda: DELETE
body: {"id": 1}


EDYCJA PLANU
uwaga: należy podać wszystkie itemy ponieważ wszystkie stare zostają usuwane
metoda: PUT
body:{
    "id_diet_plan": 0,
    "edited_items": [ 
                {
                    "food_item_id": 333,
                    "meal_time": 8,
                    "weekday": 0,
                    "food_item_weight": 100
                },
                {
                    "food_item_id": 334,
                    "meal_time": 12,
                    "weekday": 0,
                    "food_item_weight": 200
                }
            ]
}
```

#### PRZYPISANIE DIET PLANU DO CURRENT USERA  (/assign_plan):
```
headers standardowo x-access-token
body:
{
metoda: POST
body: {
"diet_plan_id": 1
}
```

#### ODPISANIE DIET PLANU OD CURRENT USERA  (/detach_plan):
```
headers standardowo x-access-token
body:
{
metoda: POST
body: {
"diet_plan_id": 1
}
```

#### ZWRACA WSZYSTKIE FOOD ITEMY  (/items):
```
headers standardowo x-access-token
```

#### ZWRACA FOOD ITEM BY ID  (/item/id):
```
headers standardowo x-access-token
```


#### TWORZENIE LUB USUWANIE FOOD ITEMA  (/item):
```
headers standardowo x-access-token

DODAWANIE
metoda: POST
body: {
"name": "item1",
"calories": 10,
"protein": 10.6, 
"fat": 10.3, 
"carbs": 10.3
}

USUWANIE:  (TYLKO ADMIN)
body: {"id": 1}
```

#### PRZYPISANIE FOOD ITEMA/ITEMÓW DO DIET PLANU  (/assign_items):
```
headers standardowo x-access-token
metoda: POST
body: {
	items": [
                {
                    "food_item_id": 33,
                    "diet_plan_id": 2,
                    "meal_time": 8,
                    "weekday": 0,
                    "food_item_weight": 100
                },
                
                {
                    "food_item_id": 34,
                    "diet_plan_id": 2,
                    "meal_time": 12,
                    "weekday": 0,
                    "food_item_weight": 200 
                }
            ] 
}
```


## API PLANÓW TRENINGOWYCH

#### TWORZENIE, USUWANIE LUB EDYCJA PLANU TRENINGOWEGO  (/training_plan):
```
headers standardowo x-access-token

DODAWANIE
metoda: POST
BODY:
{
"name": "plan utworzony przez POST",
"type": "FBW",
"our_trainings": [
                {
			    "training_id": 1,          # id naszego ćwiczenia z bazy
			    "training_series": 5,
			    "training_repeats": 9,
			    "breaks_series": 20,
			    "breaks_trainings": 120,
			    "weekday": 1
                }, {...}, ...
            ]
}


USUWANIE   (tylko ADMIN)
metoda: DELETE
body: {"id": 1}


EDYCJA PLANU
uwaga: należy podać wszystkie ćwiczenia(our_trainigs) ponieważ wszystkie stare zostają usuwane
metoda: PUT
body:
{
    "id_training_plan": 1,
    "edited_trainings": [
                {
			    "training_id": 1,          # id naszego ćwiczenia z bazy
			    "training_series": 5,
			    "training_repeats": 9,
			    "breaks_series": 20,
			    "breaks_trainings": 120,
			    "weekday": 1
                }, {...}, ...
            ]
}
```

#### ZWRACA PLANY ZALOGOWANEGO USERA (/user_train_plans): + wyjaśnienie responsea
```
headers standardowo x-access-token
metoda: GET

wyjaśnienie responsea: 
{
    "my_training_plans": [
        {
            "id_plan": 1,
            "name": "PLAN Trening 2",
            "plan_details": [
                {
                    "1": [  #tutaj 1 to dzień czyli wtorek
                        {
                            "body_part": "Klatka piersiowa",
                            "breaks_series": 20,
                            "breaks_trainings": 120,
                            "name": "Podciągnięcia",
                            "training_repeats": 12,
                            "training_series": 6
                        },
                        {
                            "body_part": "Plecy",
                            "breaks_series": 25,
                            "breaks_trainings": 180,
                            "name": "Wznosy sztangi nad głową",
                            "training_repeats": 8,
                            "training_series": 10
                        }
                    ]
                }
            ],
            "type": "Split",
            "username": "mati"
        },
        {
            "id_plan": 2,
            "name": "plan utworzony przez POST",
            "plan_details": [
                {
                    "1": [
                        {
                            "body_part": "Klatka piersiowa",
                            "breaks_series": 20,
                            "breaks_trainings": 120,
                            "name": "Podciągnięcia",
                            "training_repeats": 9,
                            "training_series": 5
                        }
                    ]
                }
            ],
            "type": "FBW",
            "username": "mati"
        }
    ]
}
```

#### ZWRACA TRAINING PLAN BY ID (/training_plan/id):
```
headers standardowo x-access-token
metoda: GET
```


#### PRZYPISANIE TRAINING PLANU DO CURRENT USERA  (/assign_training_plan):
```
headers standardowo x-access-token
body:
{
metoda: POST
body: {
"training_plan_id": 1
}
```

#### ODPISANIE TRAINING PLANU OD CURRENT USERA  (/detach_training_plan):
```
headers standardowo x-access-token
body:
{
metoda: POST
body: {
"training_plan_id": 1
}
```

#### ZWRACA WSZYSTKIE TRAININGSY  (/trainings):
```
metoda: GET
headers standardowo x-access-token
```

#### ZWRACA TRAINING BY ID  (/training/id):
```
metoda: GET
headers standardowo x-access-token
```


#### TWORZENIE LUB USUWANIE TRAININGU(ĆWICZENIA)  (/training):
```
headers standardowo x-access-token

DODAWANIE
metoda: POST
body: {
"name": "Martwy ciąg",
"body_part": "Całe ciało"
}

USUWANIE:  (TYLKO ADMIN)
body: {"id": 1}
```

#### PRZYPISANIE TRAININGU(ĆWICZENIA) DO TRAINING PLANU  (/assign_trainings):
```
headers standardowo x-access-token
metoda: POST
body: {
	"trainings": [
                {
			    "training_id": 1,          # id naszego ćwiczenia z bazy
			    "training_plan_id": 0,      # id planu do którego przypisać ćwiczenie
                "training_series": 5,
			    "training_repeats": 9,
			    "breaks_series": 20,
			    "breaks_trainings": 120,
			    "weekday": 1
                },
                {
			    "training_id": 1,
                "training_plan_id": 0,
			    "training_series": 5,
			    "training_repeats": 9,
			    "breaks_series": 20,
			    "breaks_trainings": 120,
			    "weekday": 1
                }
            ] 
}
```