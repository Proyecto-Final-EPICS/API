import mongoengine as me

class Game(me.Document):
    code = me.StringField(required=True, uniquie_with='id_school')
    name = me.StringField(required=True)
    level = me.StringField(required=True)
    topic = me.StringField()
    short_description = me.StringField(required=True)
    description = me.StringField()
    developers = me.ListField(me.DictField())
    launch_date = me.DateField()
    logo = me.URLField()
    id_school = me.IntField(required=True, unique_with='code')
    modules = me.ListField(me.DictField(), default = list)

    meta = {'collection': 'games'}