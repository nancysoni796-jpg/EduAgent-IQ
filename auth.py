from db import Database

db = Database()

def register(username, password):
    return db.add_user(username, password)

def login(username, password):
    return db.login_user(username, password)