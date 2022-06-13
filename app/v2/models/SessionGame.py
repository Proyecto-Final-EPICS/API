from datetime import datetime
import mongoengine as me
# from v2.utils import 

class ResumeModule(me.EmbeddedDocument):
    # "modules":[{"aproved":false,"moduleId":"module1","avrScore":{"$numberDouble":"0.0"},"avrTime":{"$numberDouble":"0.0"},"minutes":{"$numberLong":"0"}},{"aproved":false,"moduleId":"module2","avrScore":{"$numberDouble":"0.0"},"avrTime":{"$numberDouble":"0.0"},"minutes":{"$numberLong":"0"}}
    moduleId = me.StringField(required=True)
    aproved = me.BooleanField(required=True, default=False)
    score = me.FloatField(required=True, default=0.0)
    time = me.FloatField(required=True, default=0.0)

class SessionModule(me.EmbeddedDocument):
    # "modules":[{"moduleId":"module1","avrScore":{"$numberInt":"0"},"avrTime":{"$numberDouble":"0.0"},"aproved":false},{"moduleId":"module2","avrScore":{"$numberInt":"0"},"avrTime":{"$numberDouble":"0.0"},"aproved":false}]
    moduleId = me.StringField(required=True)
    aproved = me.BooleanField(required=True, default=False)
    score = me.FloatField(required=True)
    time = me.FloatField(required=True)

class Resume(me.EmbeddedDocument):
    # "resume":{"score":{"$numberDouble":"0.0"},"minutes":{"$numberLong":"0"},"numSessions":{"$numberInt":"1"},"modules":[{"aproved":false,"moduleId":"module1","avrScore":{"$numberDouble":"0.0"},"avrTime":{"$numberDouble":"0.0"},"minutes":{"$numberLong":"0"}},{"aproved":false,"moduleId":"module2","avrScore":{"$numberDouble":"0.0"},"avrTime":{"$numberDouble":"0.0"},"minutes":{"$numberLong":"0"}}]}
    score = me.FloatField(default = 0)
    time = me.FloatField(default = 0)
    numSessions = me.IntField(default = 0)
    modules = me.EmbeddedDocumentListField(ResumeModule, default = list)

class Session(me.EmbeddedDocument):
    # "sessions":[{"time":0,"date":{"$date":{"$numberLong":"1509537600000"}},"score":{"$numberInt":"0"},"id_session":{"$numberLong":"0"},"modules":[{"moduleId":"module1","avrScore":{"$numberInt":"0"},"avrTime":{"$numberDouble":"0.0"},"aproved":false},{"moduleId":"module2","avrScore":{"$numberInt":"0"},"avrTime":{"$numberDouble":"0.0"},"aproved":false}]}]
    time = me.FloatField(default = 0)
    date = me.DateField(default=datetime.utcnow)
    score = me.FloatField(default = 0)
    id_session = me.IntField(required = True)
    modules = me.EmbeddedDocumentListField(SessionModule, default = list)

class SessionGame(me.Document):
    # {"_id":{"$oid":"629d6c115f359ef240802bd8"},"user":"testSt1","date":{"$date":{"$numberLong":"1509537600000"}},"resume":{"score":{"$numberDouble":"0.0"},"minutes":{"$numberLong":"0"},"numSessions":{"$numberInt":"1"},"modules":[{"aproved":false,"moduleId":"module1","avrScore":{"$numberDouble":"0.0"},"avrTime":{"$numberDouble":"0.0"},"minutes":{"$numberLong":"0"}},{"aproved":false,"moduleId":"module2","avrScore":{"$numberDouble":"0.0"},"avrTime":{"$numberDouble":"0.0"},"minutes":{"$numberLong":"0"}}]},"game_code":"manitasPlayTest","sessions":[{"time":"00:00.000","date":{"$date":{"$numberLong":"1509537600000"}},"score":{"$numberInt":"0"},"id_session":{"$numberLong":"0"},"modules":[{"moduleId":"module1","avrScore":{"$numberInt":"0"},"avrTime":{"$numberDouble":"0.0"},"aproved":false},{"moduleId":"module2","avrScore":{"$numberInt":"0"},"avrTime":{"$numberDouble":"0.0"},"aproved":false}]}],"id_course":"CSE","id_school":"1"}
    user = me.StringField(required=True)
    date = me.DateTimeField(required=True, default= datetime.utcnow)
    resume = me.EmbeddedDocumentField(Resume, required=True, default=Resume)
    game_code = me.StringField(required=True)
    sessions = me.EmbeddedDocumentListField(Session, default=list)
    id_course = me.StringField(required=True)
    id_school = me.IntField(required=True)
    meta = {'collection': 'session_games'}
    