import mongoengine as me

class School(me.Document):
    # {"_id":{"$oid":"625b8f08f1560344a84c6f71"},"idSchool":{"$numberInt":"1"},"schoolName":"Test School","students":[{"studentName":"Test Student","age":{"$numberInt":"17"}}],"teachers":[{"professorName":"Test Professor","age":{"$numberInt":"30"},"professorId":{"$oid":"625b8f3bf1560344a84cd41f"}}],"rectors":[{"rectorID":{"$oid":"625b8f83f1560344a84d5f10"},"rectorName":"Rector"}],"contactPhone":"3268746592"}
    idSchool = me.StringField(required=True)
    schoolName = me.StringField(required=True)
    students = me.ListField(me.DictField())
    rectors = me.ListField(me.DictField())
    teachers = me.ListField(me.DictField())
    contactPhone = me.StringField(required=True)
    
    meta = {'collection': 'schools'}
    