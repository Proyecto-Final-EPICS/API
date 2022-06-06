import mongoengine as me

class Student(me.Document):
    name = me.StringField(required=True)
    description = me.StringField(required=True)
    permission_level = me.IntField(required=True)

    meta = {'collection': 'students'}
