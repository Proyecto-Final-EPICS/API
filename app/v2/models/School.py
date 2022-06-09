import mongoengine as me

class School(me.Document):
    
    id_school = me.IntField(required=True, unique=True)
    school_name = me.StringField(required=True)
    students = me.ListField(me.DictField())
    rectors = me.ListField(me.DictField())
    professors = me.ListField(me.DictField())
    contact_phone = me.DictField()
    location = me.DictField()
    courses = me.ListField(me.DictField())
    games = me.ListField(me.DictField())
    
    meta = {'collection': 'schools'}
    