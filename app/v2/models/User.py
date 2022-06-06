import mongoengine as db
from database import db

class User(db.Document):
    # {"_id":{"$oid":"625b8eddf1560344a84c1387"},"name":"Teacher1","username":"Usurio1","password":"Contraseña","role":"professor","idSchool":{"$numberInt":"1"}}
    firstname = db.StringField(required=True)
    lastname = db.StringField(required=True)
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    role = db.StringField(required=True)
    id_school = db.IntField()
    meta = {'collection': 'users'}
