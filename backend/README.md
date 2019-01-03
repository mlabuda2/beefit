
### PIERWSZE URUCHAMIANIE:
```
1. python create.py
```
### KOLEJNE URUCHAMIANIA:
```
1.'python3.6 api.py'
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
### ENDPOINT user_plans wyjaśnienie
```
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

### TWORZENIE NOWEGO DIET PLANU  (/create_plan):
```
headers standardowo x-access-token
body:
{
metoda: POST
body: {
"name": "plan1",
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


### TWORZENIE NOWEGO FOOD ITEMA  (/create_item):
```
headers standardowo x-access-token
body:
{
metoda: POST
body: {
"name": "item1",
"calories": 10,
"protein": 10.6, 
"fat": 10.3, 
"carbs": 10.3
}
```

### PRZYPISANIE FOOD ITEMA DO DIET PLANU  (/assign_item):
```
headers standardowo x-access-token
body:
{
metoda: POST
body: {
"food_item_id": 1, 
"diet_plan_id": 1,
"meal_time": 10,
"weekday": 1,
"food_item_weight": 100, #ile gram
"food_item_pieces": 2, #lub ile sztuk np jabłko 2 szt bez podawania wagi lub z wagą
}
```

TODO:
-ENDPOINT który tworzy plan i przypisuje od razu itemy w jednym requescie
 np. uzytkownik tworzy nowy plan od razu pełny z itemami itp.