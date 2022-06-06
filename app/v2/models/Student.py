import mongoengine as me

class Student(me.Document):

    age = me.IntField()
    course = me.StringField(required=True)
    address = me.StringField(required=True)
    phone = me.DictField(required=True)
    email = me.StringField(required=True)
    username = me.StringField(required=True, unique=True)
    lastname = me.StringField(required=True)
    birth_date = me.DateTimeField(required=True)
    firstname = me.StringField(required=True)
    id_school = me.IntField()
    
    meta = {'collection': 'students'}
