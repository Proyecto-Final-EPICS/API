from v2.models import School, Professor, Student, Rector
from flask import jsonify
from v2.common.authDecorators import admin_required, rector_required
from mongoengine import NotUniqueError, ValidationError
from v2.common.utils import find
from . import game, course, professor, student, rector

# MAIN REQUESTS ************************************************
def get_schools():
    return School.objects.to_json()
    
def get_school(id_school):
    try:
        return jsonify(School.objects.get(id_school=id_school))
    except School.DoesNotExist:
        return {'msg': 'School does not exist'} 

@admin_required
def post_school(content):
    try:
        id_school = content['id_school']
        School.objects.get(id_school=id_school)
        return {'msg': 'School already exists'}
    except School.DoesNotExist:
        try:
            content.pop('retors', None)
            content.pop('professors', None)
            content.pop('students', None)
            content.pop('courses', None)
            content.pop('games', None)
            
            school = School(**content)

            school.validate()
            school.save()
            
            return {'msg': 'School created successfully'}, 201
        except ValidationError:
            return {'msg': 'Invalid school data'}
        except NotUniqueError:
            return {'msg': 'Some fields required as unique are repeated'}
        except Exception as e:
            return {'msg': 'Exception', 'err': str(e)}
            
    except KeyError:
        return {'msg': 'Required fields not provided'}
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}

@admin_required
def put_school(id_school, content):
    try:
        content.pop('students', None)
        content.pop('professors', None)
        content.pop('rectors', None)
        content.pop('games', None)
        content.pop('courses', None)
        
        school = School.objects.get(id_school=id_school)
        id_school_start = school.id_school
        done = school.modify(**content) if content != {} else True

        if done:
            if school.id_school != id_school_start:
                for student_ in school.students:
                    student.edit_id_school_from_student(student_.username, school.id_school)
                for prof in school.professors:
                    professor.edit_id_school_from_professor(prof.username, school.id_school)
                for rec in school.rectors:
                    rector.edit_id_school_from_rector(rec.username, school.id_school)
                for course_ in school.courses:
                    course.edit_id_school_from_course(id_school_start, course_.code, school.id_school)
                for game_ in school.games:
                    game.edit_id_school(id_school_start, game_.code, school.id_school)
                
            return school.to_json()
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
def add_professor_to_school(id_school, prof):
    try:
        return add_professor(School.objects.get(id_school=id_school), prof)
    except School.DoesNotExist:
        return False

def add_professor(school, prof):
    try:
        school.professors.append(prof)
        school.save()
        return True
    except ValidationError:
        return False

def edit_professor_from_school(id_school, username, prof):
    try:
        return edit_professor(School.objects.get(id_school=id_school), username, prof)
    except School.DoesNotExist:
        return False

def edit_professor(school, username, prof):
    try:
        i = find(school.professors, lambda p: p['username'] == username)
        if i == -1: return False
        
        school.professors[i] = prof
        school.save()
        return True
    except ValidationError:
        return False

def del_professor_from_school(id_school, username):
    try:
        return del_professor(School.objects.get(id_school=id_school), username)
    except School.DoesNotExist:
        return False

def del_professor(school, username):
    try:
        i = find(school.professors, lambda p: p['username'] == username)
        if i == -1: return False

        school.professors.pop(i)
        school.save()
        return True
    except ValidationError:
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
def add_rector_to_school(id_school, rec):
    try:
        return add_rector(School.objects.get(id_school=id_school), rec)
    except School.DoesNotExist:
        return False

def add_rector(school, rec):
    try:
        school.rectors.append(rec)
        school.save()
        return True
    except ValidationError:
        return False

def edit_rector_from_school(id_school, username, rec):
    try:
        return edit_rector(School.objects.get(id_school=id_school), username, rec)
    except School.DoesNotExist:
        return False

def edit_rector(school, username, rec):
    try:
        i = find(school.rectors, lambda p: p['username'] == username)
        if i == -1: return False
        
        school.rectors[i] = rec
        school.save()
        return True
    except ValidationError:
        return False

def del_rector_from_school(id_school, username):
    try:
        return del_rector(School.objects.get(id_school=id_school), username)
    except School.DoesNotExist:
        return False

def del_rector(school, username):
    try:
        i = find(school.rectors, lambda p: p['username'] == username)
        if i == -1: return False

        school.rectors.pop(i)
        school.save()
        return True
    except ValidationError:
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
def add_student_to_school(id_school, student):
    try:
        return add_student(School.objects.get(id_school=id_school), student)
    except School.DoesNotExist:
        return False

def add_student(school, student):
    try:
        school.students.append(student)
        school.save()
        return True
    except ValidationError:
        return False

def edit_student_from_school(id_school, username, student):
    try:
        return edit_student(School.objects.get(id_school=id_school), username, student)
    except School.DoesNotExist:
        return False

def edit_student(school, username, student):
    try:
        i = find(school.students, lambda p: p['username'] == username)
        if i == -1: return False

        school.students[i] = student
        school.save()
        return True
    except ValidationError:
        return False

def del_student_from_school(id_school, username):
    try:
        return del_student(School.objects.get(id_school=id_school), username)
    except School.DoesNotExist:
        return False

def del_student(school, username):
    try:
        i = find(school.students, lambda p: p['username'] == username)
        if i == -1: return False
        
        school.students.pop(i)
        school.save()
        return True
    except ValidationError:
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
def add_course_to_school(id_school, course):
    try:
        return add_course(School.objects.get(id_school=id_school), course)
    except School.DoesNotExist:
        return False

def add_course(school, course):
    try:
        school.courses.append(course)
        school.save()
        return True
    except ValidationError:
        return False

def edit_course_from_school(id_school, course_code, course):
    try:
        return edit_course(School.objects.get(id_school=id_school), course_code, course)
    except School.DoesNotExist:
        return False

def edit_course(school, course_code, course):
    try:
        i = find(school.courses, lambda p: p['code'] == course_code)
        if i == -1: return False

        school.courses[i] = course
        school.save()
        return True
    except ValidationError:
        return False

def del_course_from_school(id_school, course_code):
    try:
        return del_course(School.objects.get(id_school=id_school), course_code)
    except School.DoesNotExist:
        return False

def del_course(school, course_code):
    try:
        i = find(school.courses, lambda p: p['code'] == course_code)
        if i == -1: return False

        school.courses.pop(i)
        school.save()
        return True
    except ValidationError:
        return False

# Game
def add_game_to_school(id_school, game):
    try:
        return add_game(School.objects.get(id_school=id_school), game)
    except School.DoesNotExist:
        return False

def add_game(school, game):
    try:
        school.games.append(game)
        school.save()
        return True
    except ValidationError:
        return False

def edit_game_from_school(id_school, game_code, game):
    try:
        return edit_game(School.objects.get(id_school=id_school), game_code, game)
    except School.DoesNotExist:
        return False

def edit_game(school, game_code, game):
    try:
        i = find(school.games, lambda p: p['code'] == game_code)
        if i == -1: return False

        school.games[i] = game
        school.save()
        return True
    except ValidationError:
        return False

def del_game_from_school(id_school, game_code):
    try:
        return del_game(School.objects.get(id_school=id_school), game_code)
    except School.DoesNotExist:
        return False

def del_game(school, game_code):
    try:
        i = find(school.games, lambda p: p['code'] == game_code)
        if i == -1: return False

        school.games.pop(i)
        school.save()
        return True
    except ValidationError:
        return False
