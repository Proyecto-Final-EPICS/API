import mongoengine as me

class Course(me.Document):
    code = me.StringField(required=True, unique_with='id_school')
    id_school = me.IntField(required=True, unique_with='code')
    name = me.StringField(required=True)
    professors = me.ListField(me.DictField(), default=list)
    level = me.StringField(default='-')
    period = me.StringField(required=True)
    students = me.ListField(me.DictField(), deafult=list)
    games = me.ListField(me.DictField(), default=list)
    
    meta = {'collection': 'courses'}