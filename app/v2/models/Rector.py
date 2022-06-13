import mongoengine as me
from random import random, randrange

class Rector(me.Document):
    username = me.StringField(required=True, unique=True)
    firstname = me.StringField(required=True)
    lastname = me.StringField(required=True)
    id_school = me.IntField(required=True)
    identity_doc = me.StringField(required=True, unique=True)
    birth_date = me.DateField(required=True)
    email = me.StringField()
    phone = me.DictField()
    gender = me.StringField()
    age = me.IntField()
    photo = me.URLField(default='https://randomuser.me/api/portraits/{}men/{}.jpg'.format(
        'wo' if random() < 0.5 else '',
        randrange(0, 100)
    ))
    meta = {'collection': 'rectors'}
