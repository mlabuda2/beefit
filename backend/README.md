
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
        "0": {              
            "8": [          

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