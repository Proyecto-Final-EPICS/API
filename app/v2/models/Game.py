from email.policy import default
import mongoengine as me

class GameModule(me.EmbeddedDocument):
    name = me.StringField(required=True)
    num_questions = me.IntField(required=True)


class Game(me.Document):
    code = me.StringField(required=True, uniquie_with='id_school')
    name = me.StringField(required=True)
    level = me.StringField(required=True)
    topic = me.StringField()
    short_description = me.StringField(required=True)
    description = me.StringField()
    developers = me.ListField(me.DictField())
    launch_date = me.DateField()
    logo = me.URLField(default = 'https://cdn.pixabay.com/photo/2016/12/23/07/00/game-1926906_960_720.png')
    id_school = me.IntField(required=True, unique_with='code')
    modules = me.EmbeddedDocumentListField(GameModule, default=list)

    meta = {'collection': 'games'}