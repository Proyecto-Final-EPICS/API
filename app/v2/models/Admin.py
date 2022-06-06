import mongoengine as me

class Admin(me.Document):
    name = me.StringField(required=True)
    username = me.StringField(required=True)
    email = me.StringField()
    phone = me.DictField()

    meta = {'collection': 'admins'}
