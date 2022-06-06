import mongoengine as me

class Professor(me.Document):
    id_school = me.IntField(required=True)
    username = me.StringField(required=True)
    firstname = me.StringField(required=True)
    lastname = me.StringField(required=True)
    email = me.StringField()
    phone = me.DictField()
    gender = me.StringField()
    birth_date = me.DateField(required=True)
    age = me.IntField()
    photo = me.URLField()
    department = me.StringField()
    courses = me.ListField(me.DictField())

    meta = {'collection': 'professors'}
