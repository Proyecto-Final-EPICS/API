import mongoengine as db
from database import db

class User(db.Document):
    username = db.StringField(required=True, unique=True)
    firstname = db.StringField(required=True)
    lastname = db.StringField(required=True)
    password = db.StringField(required=True)
    role = db.StringField(required=True)
    id_school = db.IntField(required=True)
    meta = {'collection': 'users'}
