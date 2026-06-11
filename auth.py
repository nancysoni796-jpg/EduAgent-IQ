from db import Database

db = Database()

def register(username, password):
    return db.add_user(username, password)

def login(username, password):
    return db.login_user(username, password)
from db import Database

_db = Database()

def register(username, password):
    return _db.add_user(username, password)

def login(username, password):
    return _db.login_user(username, password)