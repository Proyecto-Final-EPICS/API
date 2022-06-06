import mongoengine as me

class Rector(me.Document):
    id_school = me.StringField(required=True)
    username = me.StringField(required=True)
    firstname = me.StringField(required=True)
    lastname = me.StringField(required=True)
    email = me.StringField()
    phone = me.StringField()
    gender = me.StringField()
    birth_date = me.DateField(required=True)
    age = me.IntField()
    phone = me.DictField()

    meta = {'collection': 'rectors'}
