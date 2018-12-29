
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
        "0": {              # tutaj 0 to dzień tygodnia
            "8": [          # tutaj 8 to godzina posiłku
                "tuńczyk",
                100,        # ta wartość to ilość posiłku - gramy/ml
                2           # ta wartość to ilość posiłku - sztuki         jedno z tego może być Null ale nie musi
            ],
            "16": [
                "tuńczyk",
                350,
                5,
                "kurczak",
                1100,
                1
            ]
        },
        "1": {
            "10": [
                "tuńczyk",
                300,
                4
            ]
        }
```