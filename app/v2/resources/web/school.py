from v2.models import School, Professor, Student, Rector
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
def add_professor(id_school, prof):
    try:
        school = School.objects.get(id_school=id_school)
        school.professors.append({
            'firstname': prof.firstname,
            'lastname': prof.lastname,
            'username': prof.username,
            'department': prof.department,
            'photo': prof.photo,
        })
        school.save()
        return True
    except (School.DoesNotExist, ValidationError):
        return False

def edit_professor(id_school, username, prof):
    try:
        school = School.objects.get(id_school=id_school)
        school.professors[find(school.professors, lambda p: p['username'] == username)] = {
            'firstname': prof.firstname,
            'lastname': prof.lastname,
            'username': prof.username,
            'department': prof.department,
            'photo': prof.photo,
        }
        school.save()
        return True
    except (School.DoesNotExist, ValidationError):
        return False

def del_professor(id_school, username):
    try:
        school = School.objects.get(id_school=id_school)
        school.professors.pop(find(school.professors, lambda p: p['username'] == username))
        school.save()
        return True
    except (School.DoesNotExist, ValidationError):
        return False

# def update_professors(id_school):
#     try:
#         profs = Professor.objects(id_school=id_school)
#         return School.objects.get(id_school=id_school).modify(
#             professors=list(map(lambda x: {
#                 'username': x.username,
#                 'firstname': x.firstname,
#                 'lastname': x.lastname,
#                 'department': x.department,
#             }, profs))
#         )
#     except (School.DoesNotExist, Professor.DoesNotExist):
#         return False

# Rector
def add_rector(id_school, rec):
    try:
        school = School.objects.get(id_school=id_school)
        school.rectors.append({
            'firstname': rec.firstname,
            'lastname': rec.lastname,
            'username': rec.username,
            'photo': rec.photo,
        })
        school.save()
        return True
    except (School.DoesNotExist, ValidationError):
        return False

def edit_rector(id_school, username, rec):
    try:
        school = School.objects.get(id_school=id_school)
        school.rectors[find(school.rectors, lambda p: p['username'] == username)] = {
            'firstname': rec.firstname,
            'lastname': rec.lastname,
            'username': rec.username,
            'photo': rec.photo,
        }
        school.save()
        return True
    except (School.DoesNotExist, ValidationError):
        return False

def del_rector(id_school, username):
    try:
        school = School.objects.get(id_school=id_school)
        school.rectors.pop(find(school.rectors, lambda p: p['username'] == username))
        school.save()
        return True
    except (School.DoesNotExist, ValidationError):
        return False

# def update_rectors(id_school, rectors):
#     try:
#         return School.objects.get(id_school=id_school).modify(
#             rectors=list(map(lambda x: {
#                 'username': x.username,
#                 'firstname': x.firstname,
#                 'lastname': x.lastname,
#             }, rectors))
#         )
#     except School.DoesNotExist:
#         return False

# Student
def add_student(id_school, student):
    try:
        school = School.objects.get(id_school=id_school)
        school.students.append({
            'firstname': student.firstname,
            'lastname': student.lastname,
            'username': student.username,
            'photo': student.photo,
        })
        school.save()
        return True
    except (School.DoesNotExist, ValidationError):
        return False

def edit_student(id_school, username, student):
    try:
        school = School.objects.get(id_school=id_school)
        school.students[find(school.students, lambda p: p['username'] == username)] = {
            'firstname': student.firstname,
            'lastname': student.lastname,
            'username': student.username,
            'photo': student.photo,
        }
        school.save()
        return True
    except (School.DoesNotExist, ValidationError):
        return False

def del_student(id_school, username):
    try:
        school = School.objects.get(id_school=id_school)
        school.students.pop(find(school.students, lambda p: p['username'] == username))
        school.save()
        return True
    except (School.DoesNotExist, ValidationError):
        return False

# def update_students(id_school, students):
#     try:
#         return School.objects.get(id_school=id_school).modify(
#             students=list(map(lambda x: {
#                 'username': x.username,
#                 'firstname': x.firstname,
#                 'lastname': x.lastname,
#             }, students))
#         )
#     except School.DoesNotExist:
#         return False

# Course
def add_course(id_school, course):
    try:
        school = School.objects.get(id_school=id_school)
        school.courses.append({
            'code': course.code,
            'name': course.name,
        })
        school.save()
        return True
    except (School.DoesNotExist, ValidationError):
        return False

def edit_course(id_school, course_code, course):
    try:
        school = School.objects.get(id_school=id_school)
        school.courses[find(school.courses, lambda p: p['code'] == course_code)] = {
            'code': course.code,
            'name': course.name,
        }
        school.save()
        return True
    except (School.DoesNotExist, ValidationError):
        return False

def del_course(id_school, course_code):
    try:
        school = School.objects.get(id_school=id_school)
        school.courses.pop(find(school.courses, lambda p: p['code'] == course_code))
        school.save()
        return True
    except (School.DoesNotExist, ValidationError):
        return False
