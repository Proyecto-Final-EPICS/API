import mongoengine as me

class User(me.Document):
    # {"_id":{"$oid":"625b8eddf1560344a84c1387"},"name":"Teacher1","username":"Usurio1","password":"Contraseña","role":"professor","idSchool":{"$numberInt":"1"}}
    name = me.StringField(required=True)
    username = me.StringField(required=True)
    password = me.StringField(required=True)
    role = me.StringField(required=True)
    idSchool = me.StringField(required=True)
    meta = {'collection': 'users'}
