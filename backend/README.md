
### PIERWSZE URUCHAMIANIE:
```
1. python create.py
```
### KOLEJNE URUCHAMIANIA:
```
1.'python manage.py run'
```
### LOGOWANIE ADMIN
```
(postman)
Basic Auth
U: mati
P: mati
otrzymujemy token
```
### DZIAŁANIA Z TOKENEM
```
header: 
    key: x-access-token
    value: "tutaj otrzymany token"
```
### REJESTRACJA NOWEGO UŻYTKOWNIKA (/register):
```
metoda: POST
body: {
"username": "user1",
"email": "user1@user.pl",
"password": "user1"
}
```
### ZWRACA PLANY ZALOGOWANEGO USERA (/user_plans): + wyjaśnienie responsea
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

### ZWRACA DIET PLAN BY ID (/plan/id):
```
headers standardowo x-access-token
metoda: GET
```

### TWORZENIE NOWEGO DIET PLANU  (/create_plan):
```
headers standardowo x-access-token
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
```

### PRZYPISANIE DIET PLANU DO USERA  (/assign_plan):
```
headers standardowo x-access-token
body:
{
metoda: POST
body: {
"user_id": 1,
"diet_plan_id": 1
}
```

### ZWRACA WSZYSTKIE FOOD ITEMY  (/items):
```
headers standardowo x-access-token
```

### ZWRACA FOOD ITEM BY ID  (/item/id):
```
headers standardowo x-access-token
```


### TWORZENIE LUB USUWANIE FOOD ITEMA  (/item):
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

USUWANIE:
body: {id: 1}
```

### PRZYPISANIE FOOD ITEMA/ITEMÓW DO DIET PLANU  (/assign_items):
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

Do rozważenia:
-czy w fooditem nie dodać public_id generowane na froncie?
    korzyści:
        -można dodać custom item do planu przed dodaniem do bazy, a jeśli go nie ma to trzeba najpierw
        zacommitować go do bazy i dopiero wtedy tworzy się auto id po którym można dodać do planu item