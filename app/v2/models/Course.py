import mongoengine as me

class Course(me.Document):
    code = me.StringField(required=True)
    id_school = me.IntField(required=True)
    name = me.StringField(required=True)
    professors = me.ListField(me.DictField())
    level = me.StringField()
    period = me.StringField(required=True)
    students = me.ListField(me.DictField())
    games = me.ListField(me.DictField())
    
    meta = {'collection': 'courses'}