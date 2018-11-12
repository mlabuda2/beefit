
### PIERWSZE URUCHAMIANIE:
```
1.'python3.6'
2.>>'from api import db'
3.>>'db.create_all()'
4.>>'exit()'
5.'python3.6 api.py'
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
