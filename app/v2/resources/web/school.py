from v2.models import School
from mongoengine import NotUniqueError, ValidationError, OperationError
from flask import jsonify

def getSchool(id):
    return School.objects.get(id=id).to_json()

def postSchool(content):
    school = School(**content)
    try:
        school.save()
        return school.to_json()
    except NotUniqueError:
        return jsonify(msg='School already exists')
    except ValidationError:
        return jsonify(msg='Invalid data')

def delSchool(id):
    try:
        School.objects.get(id=id).delete()
        return jsonify(msg='School deleted')
    except School.DoesNotExist:
        return jsonify(msg='School does not exist')
    except OperationError:
        return jsonify(msg='School cannot be deleted')

def updateSchool(id, content):
    try:
        school = School.objects.get(id=id)
        school.update(**content)
        return school.to_json()
    except School.DoesNotExist:
        return jsonify(msg='School does not exist')
    except ValidationError:
        return jsonify(msg='Invalid data')