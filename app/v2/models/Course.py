import mongoengine as me

class Course(me.Document):
    code = me.StringField(required=True)
    school = me.StringField(required=True)
    name = me.StringField(required=True)
    professors = me.ListField(me.DictField())
    level = me.StringField(required=True)
    period = me.StringField(required=True)
    students = me.ListField(me.DictField())
    games = me.ListField(me.DictField())
    
    meta = {'collection': 'courses'}