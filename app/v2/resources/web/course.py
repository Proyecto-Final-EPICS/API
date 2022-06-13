from mongoengine import NotUniqueError, ValidationError, DoesNotExist
from flask import jsonify
from v2.models import Course, Professor, Student, School
from v2.common import authDecorators, find
from . import school, professor, student

# get all courses of a school
# @authDecorators.school_member_required
def get_school_courses(id_school):
    return Course.objects(id_school=id_school).to_json()

# get a course of a school
# @authDecorators.school_member_required
def get_school_course(id_school, course_code):
    try:
        return Course.objects.get(id_school=id_school, code=course_code).to_json()
    except DoesNotExist:
        return {'msg': 'Course does not exist'}

# create a course in a school
@authDecorators.rector_or_admin_required
def post_course(id_school, content):
    try:
        Course.objects.get(id_school=id_school, code=content['code'])
        return {'msg': 'Course already exists'}, 400
    except Course.DoesNotExist:
        try:
            school_ = School.objects.get(id_school=id_school)

            content.pop('students', None)
            content.pop('professors', None)
            content.pop('games', None)

            course = Course(**content)

            course.validate()
            course.save()
            school.add_course(school_, {
                'code': course.code,
                'name': course.name,
                'level': course.level,
            })
            
            return {'msg': 'Course created successfully'}, 201

        except School.DoesNotExist:
            return {'msg': 'Invalid school'}
        except ValidationError:
            return {'msg': 'Invalid Data'}, 401
        except NotUniqueError:
            return {'msg': 'Not unique course'}, 401
        except Exception as e:
            return {'msg': 'Exception', 'err': str(e)}, 500
    
    except KeyError as e: 
        return {'msg': 'Required fields not provided', 'err': str(e)}
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}, 500

# Update a course of a school
@authDecorators.school_member_required
def put_course(id_school, course_code, content):
    try:
        content.pop('id_school', None)
        content.pop('games', None)
        content.pop('students', None)
        content.pop('professors', None)

        course = Course.objects.get(id_school=id_school, code=course_code)
        done = course.modify(**content) if content != {} else True
        if not done: return {'msg': 'The database doesn\'t match the query'}
        
        school.edit_course_from_school(id_school, course_code, {
            'code': course.code,
            'name': course.name,
            'level': course.level,
        })
        
        for prof in course.professors:
            professor.edit_course_from_professor(prof['username'], course_code, {
                'code': course.code,
                'name': course.name,
                'level': course.level,
            })
        for student_ in course.students:
            student.edit_course_from_student(student_['username'], course.code)

        return {'msg': 'Course edited successfully'}, 201
    
    except Course.DoesNotExist:
        return {'msg': 'Course does not exist'}
    except NotUniqueError:
        return {'msg': 'Some fields required as unique are repeated'}
    except KeyError:
        return {'msg': 'Required fields not provided'}
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}

# delete a course of a school
@authDecorators.school_member_required
def delete_course(id_school, course_code):
    try:
        course = Course.objects.get(id_school=id_school, code=course_code)
        course.delete()
        
        school.del_course_from_school(id_school, course_code)
        
        for prof in course.professors:
            professor.del_course_from_professor(prof['username'], course_code)
        for student_ in course.students:
            student.del_course_from_student(student_['username'])

        return {'msg': 'Course deleted successfully'}, 201
    
    except Course.DoesNotExist:
        return {'msg': 'Course does not exist'}
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}

# FIELDS ***********************************************

# Student
def add_student_to_course(id_school, course_code, student):
    try:
        return add_student(Course.objects.get(id_school=id_school, code=course_code), student)
    except Course.DoesNotExist:
        return False

def add_student(course, student):
    try:
        course.students.append(student)
        course.save()
        return True
    except ValidationError:
        return False

def edit_student_from_course(id_school, course_code, username, student):
    try:
        return edit_student(Course.objects.get(id_school=id_school, code=course_code), username, student)
    except Course.DoesNotExist:
        return False

def edit_student(course, username, student):
    try:
        i = find(course.students, lambda p: p['username'] == username)
        if i == -1: return False

        course.students[i] = student
        course.save()
        return True
    except ValidationError:
        return False

def del_student_from_course(id_school, course_code, username):
    try:
        return del_student(Course.objects.get(id_school=id_school, code=course_code), username)
    except Course.DoesNotExist:
        return False

def del_student(course, username):
    try:
        i = find(course.students, lambda p: p['username'] == username)
        if i == -1: return False

        course.students.pop(i)
        course.save()
        return True
    except ValidationError:
        return False

# Professor
def add_professor_to_course(id_school, course_code, prof):
    try:
        return add_professor(Course.objects.get(id_school=id_school, code=course_code), prof)
    except Course.DoesNotExist:
        return False

def add_professor(course, prof):
    try:
        course.professors.append(prof)
        course.save()
        return True
    except ValidationError:
        return False

def edit_professor_from_course(id_school, course_code, username, prof):
    try:
        return edit_professor(Course.objects.get(id_school=id_school, code=course_code), username, prof)
    except (Course.DoesNotExist, ValidationError):
        return False

def edit_professor(course, username, prof):
    try:
        i = find(course.professors, lambda p: p['username'] == username)
        if i == -1: return False

        course.professors[i] = prof
        course.save()
        return True
    except ValidationError:
        return False

def del_professor_from_course(id_school, course_code, username):
    try:
        return del_professor(Course.objects.get(id_school=id_school, code=course_code), username)
    except Course.DoesNotExist:
        return False

def del_professor(course, username):
    try:
        i = find(course.professors, lambda p: p['username'] == username)
        if i == -1: return False

        course.professors.pop(i)
        course.save()
        return True
    except ValidationError:
        return False

# def update_professors(id_school, course_code):
#     try:
#         profs = list(filter(lambda x: (
#             # course_code in map(lambda c: c['code'], x.courses)
#             course_code in [c['code'] for c in x.courses]
#         ), Professor.objects(id_school=id_school)))
#         return Course.objects.get(id_school=id_school).modify(
#             professors=list(map(lambda x: {
#                 'username': x.username,
#                 'firstname': x.firstname,
#                 'lastname': x.lastname,
#                 'photo': x.photo,
#             }, profs))
#         )
#     except (Course.DoesNotExist, Professor.DoesNotExist):
#         return False

# Game
def add_game_to_course(id_school, course_code, game):
    try:
        return add_game(Course.objects.get(id_school=id_school, code=course_code), game)
    except Course.DoesNotExist:
        return False

def add_game(course, game):
    try:
        course.games.append(game)
        course.save()
        return True
    except ValidationError:
        return False

def edit_game_from_course(id_school, course_code, game_code, game):
    try:
        return edit_game(Course.objects.get(id_school=id_school, code=course_code), game_code, game)
    except Course.DoesNotExist:
        return False

def edit_game(course, game_code, game):
    try:
        i = find(course.games, lambda p: p['code'] == game_code)
        if i == -1: return False

        course.games[i] = game
        course.save()
        return True
    except ValidationError:
        return False

def del_game_from_course(id_school, course_code, game_code):
    try:
        return del_game(Course.objects.get(id_school=id_school, code=course_code), game_code)
    except Course.DoesNotExist:
        return False

def del_game(course, game_code):
    try:
        i = find(course.games, lambda p: p['code'] == game_code)
        if i == -1: return False

        course.games.pop(i)
        course.save()
        return True
    except ValidationError:
        return False

# School
def edit_id_school_from_course(id_school, course_code, id_school_new):
    try:
        return edit_id_school(Course.objects.get(id_school=id_school, course=course_code), id_school_new)
    except Course.DoesNotExist:
        return False

def edit_id_school(course, id_school_new):
    try:
        course.id_school = id_school_new
        course.save()
        return True
    except ValidationError:
        return False
