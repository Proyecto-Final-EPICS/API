import mongoengine as me

class Representative(me.EmbeddedDocument):
    firstname = me.StringField(required=True)
    lastname = me.StringField(required=True)
    identity_doc = me.StringField(required=True)
    phone = me.DictField()

class Student(me.Document):
    username = me.StringField(required=True, unique=True)
    firstname = me.StringField(required=True)
    lastname = me.StringField(required=True)
    id_school = me.IntField(required=True)
    course = me.StringField(required=True)
    identity_doc = me.StringField(required=True, unique=True)
    doc_type = me.StringField(required=True)
    birth_date = me.DateTimeField(required=True)
    age = me.IntField()
    address = me.StringField()
    phone = me.DictField()
    email = me.StringField()
    legal_rep = me.EmbeddedDocumentField(Representative)
    
    meta = {'collection': 'students'}
