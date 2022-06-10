from v2.models import School
from flask import jsonify
from v2.common.authDecorators import admin_required, rector_required
from mongoengine import NotUniqueError, ValidationError
from v2.common.utils import find

# MAIN REQUESTS ************************************************
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
def put_school(id_school, content):
    try:
        school = School.objects.get(id_school=id_school)
        done = school.modify(**content) if content != {} else True

        if done: return school.to_json()
        return {'msg': 'The database doesn\'t match the query'}
        
    except School.DoesNotExist:
        return {'msg': 'School does not exist'}
    except NotUniqueError:
        return {'msg': 'Some fields required as unique are repeated'}
    except KeyError:
        return {'msg': 'Required fields not provided'}

@admin_required
def delete_school(id_school):
    try:
        School.objects.get(id_school=id_school).delete()
        return School.objects.to_json()

    except School.DoesNotExist: return {'msg': 'Non existing school'}

# FIELDS ************************************************

# Professor
def add_professor(prof):
    school = School.objects.get(id_school=prof.id_school)
    school.professors.append({
        'firstname': prof.firstname,
        'lastname': prof.lastname,
        'username': prof.username,
        'department': prof.department
    })
    school.save()

def edit_professor(username, prof):
    school = School.objects.get(id_school=prof.id_school)
    school.professors[find(school.professors, lambda p: p['username'] == username)] = {
        'firstname': prof.firstname,
        'lastname': prof.lastname,
        'username': prof.username,
        'department': prof.department
    }
    school.save()

def del_professor(prof):
    school = School.objects.get(id_school=prof.id_school)
    school.professors.pop(find(school.professors, lambda p: p['username'] == prof.username))
    school.save()

# Rector
def add_rector(rec):
    school = School.objects.get(id_school=rec.id_school)
    school.rectors.append({
        'firstname': rec.firstname,
        'lastname': rec.lastname,
        'username': rec.username,
    })

def edit_rector(username, rec):
    school = School.objects.get(id_school=rec.id_school)
    school.rectors[find(school.rectors, lambda r: r['username'] == username)] = {
        'firstname': rec.firstname,
        'lastname': rec.lastname,
        'username': rec.username,
    }
    school.save()

def del_rector(rec):
    school = School.objects.get(id_school=rec.id_school)
    school.rectors.pop(find(school.rectors, lambda r: r['username'] == rec.username))
    school.save()

# Student
def add_student(student):
    school = School.objects.get(id_school=student.id_school)
    school.students.append({
        'firstname': student.firstname,
        'lastname': student.lastname,
        'username': student.username,
    })
    school.save()

def edit_student(username, student):
    school = School.objects.get(id_school=student.id_school)
    school.students[find(school.students, lambda s: s['username'] == username)] = {
        'firstname': student.firstname,
        'lastname': student.lastname,
        'username': student.username,
    }
    school.save()

def del_student(student):
    school = School.objects.get(id_school=student.id_school)
    school.students.pop(find(school.students, lambda s: s['username'] == student.username))
    school.save()
    
# Course
def add_course(course):
    school = School.objects.get(id_school=course.id_school)
    school.courses.append({
        'code': course.code,
        'name': course.name,
    })
    school.save()

def edit_course(code, course):
    school = School.objects.get(id_school=course.id_school)
    school.courses[find(school.courses, lambda c: c['code'] == code)] = {
        'code': course.code,
        'name': course.name,
    }
    school.save()

def del_course(course):
    school = School.objects.get(id_school=course.id_school)
    school.courses.pop(find(school.courses, lambda c: c['code'] == course.code))
    school.save()
    