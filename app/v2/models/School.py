import mongoengine as me

class School(me.Document):
    
    idSchool = me.IntField(required=True, unique=True)
    schoolName = me.StringField(required=True)
    students = me.ListField(me.DictField())
    rectors = me.ListField(me.DictField())
    teachers = me.ListField(me.DictField())
    contactPhone = me.DictField(required=True)
    
    meta = {'collection': 'schools'}
    