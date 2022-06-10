from v2.models import School
from flask import jsonify
from v2.common.authDecorators import admin_required, rector_required
from mongoengine import NotUniqueError, ValidationError

def get_schools():
    return School.objects.to_json()
    
def get_school(id_school):
    try:
        return School.objects.get(id_school=id_school).to_json()
    except School.DoesNotExist:
        return {'msg': 'School does not exist'} 

@admin_required
def post_school(content):
    try:
        id_school = content['id_school']
        
        try:
            School.objects.get(id_school=id_school)
            return {'msg': 'School already exists'}
        except School.DoesNotExist:
            
            school = School(
                id_school=id_school, school_name = content['school_name'],
                contact_phone = content.get('contact_phone', {}), 
                location=content.get('location', {}),
                rectors=content.get('rectors', []), 
                professors=content.get('professors', []),
                students=content.get('students', []),
                courses=content.get('courses', []),
                games=content.get('games', []),
            )
            
            try:
                school.validate()
                school.save()
            except ValidationError:
                return {'msg': 'Invalid school data'}
            except NotUniqueError:
                return {'msg': 'Some fields required as unique are repeated'}
            
            return jsonify(school)
    except KeyError: return {'msg': 'Required fields not provided'}

@admin_required
def delete_school(id_school):
    try:
        School.objects.get(id_school=id_school).delete()
        return School.objects.to_json()

    except School.DoesNotExist: return {'msg': 'Non existing school'}

@admin_required
def put_school(id_school, content):
    try:
        school = School.objects.get(id_school=id_school)
        school.modify(content)
        
        return school.to_json()

    except School.DoesNotExist:
        return {'msg': 'School does not exist'}
    except NotUniqueError:
        return {'msg': 'Some fields required as unique are repeated'}
    except KeyError:
        return {'msg': 'Required fields not provided'}
