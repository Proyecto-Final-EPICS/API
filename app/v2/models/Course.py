import mongoengine as me

class Course(me.Document):
    code = me.StringField(required=True, unique_with='id_school')
    id_school = me.IntField(required=True, unique_with='code')
    name = me.StringField(required=True)
    period = me.StringField(required=True)
    level = me.StringField()
    capacity = me.IntField()
    professors = me.ListField(me.DictField(), default=list)
    students = me.ListField(me.DictField(), deafult=list)
    games = me.ListField(me.DictField(), default=list)
    meta = {'collection': 'courses'}