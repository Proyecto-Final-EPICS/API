import mongoengine as me

class SessionGame(me.Document):
    # {"_id":{"$oid":"629d6c115f359ef240802bd8"},"user":"testSt1","-school":"1","-course":"CSE","date":"2017-11-01T12:00:00.000Z","resume":{"score":"0","hours":"0h","numSessions":"1","modules":[{"aproved":"false","moduleId":"module1","avrScore":{"$numberInt":"0"},"avrTime":"00:00.000","hours":"0h"},{"aproved":"false","moduleId":"module2","avrScore":{"$numberInt":"0"},"avrTime":"00:00.000","hours":"0h"}]},"game_code":"manitasPlayTest","sessions":[{"time":"00:00.000","score":{"$numberInt":"0"},"modules":[{"moduleId":"module1","avrScore":{"$numberInt":"0"},"avrTime":"00:00.000"},{"moduleId":"module2","avrScore":{"$numberInt":"0"},"avrTime":"00:00.000","-aproved":false}]}]}
    user = me.StringField(required=True)
    school = me.StringField(required=True)
    course = me.StringField(required=True)
    date = me.StringField(required=True)
    resume = me.DictField(required=True)
    game_code = me.StringField(required=True)
    sessions = me.ListField(me.DictField())

    meta = {'collection': 'session_games'}