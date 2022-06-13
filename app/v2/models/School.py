import mongoengine as me

class School(me.Document):
    
    id_school = me.IntField(required=True, unique=True)
    school_name = me.StringField(required=True)
    contact_phone = me.DictField()
    location = me.DictField()
    students = me.ListField(me.DictField(), default=list)
    rectors = me.ListField(me.DictField(), default=list)
    professors = me.ListField(me.DictField(), default=list)
    courses = me.ListField(me.DictField(), default=list)
    games = me.ListField(me.DictField(), default=list)
    
    meta = {'collection': 'schools'}
    