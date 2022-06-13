from email.policy import default
import mongoengine as me

class Game(me.Document):
    code = me.StringField(required=True, unique_with='id_school')
    id_school = me.IntField(required=True, unique_with='code')
    name = me.StringField(required=True)
    level = me.StringField(required=True)
    short_description = me.StringField(required=True)
    description = me.StringField()
    topic = me.StringField()
    launch_date = me.DateField()
    logo = me.URLField(default='https://cdn.pixabay.com/photo/2016/12/23/07/00/game-1926906_960_720.png')
    modules = me.ListField(me.DictField(), default = list)
    devs = me.ListField(me.DictField(), default=list)
    meta = {'collection': 'games'}