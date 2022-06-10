import mongoengine as me

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
    photo = me.URLField()
    meta = {'collection': 'rectors'}
