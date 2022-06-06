import mongoengine as me

class Role(me.Document):
    name = me.StringField(required=True)
    description = me.StringField(required=True)
    permision_level = me.IntField(required=True)

    meta = {'collection': 'roles'}
