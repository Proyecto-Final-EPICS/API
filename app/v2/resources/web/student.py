from flask import jsonify
from mongoengine import NotUniqueError, ValidationError
from dateutil.parser import isoparse
from random import randrange, random
from v2.common.utils import age_from_birth_date, find
from v2.models import Student, User, School, Course
from v2.common.authDecorators import role_permission_required
from . import school, course

def get_school_students(id_school):
    return Student.objects(id_school=id_school).to_json()

# def get_school_student(id_school, username):
#     return Student.objects.get(username=username)

# @role_permission_required('>')
def post_student(content):
    try:
        User.objects.get(username=content['username'])
        return {'msg': 'User already exists'}
    except User.DoesNotExist:
        try:
            school_ = School.objects.get(id_school=content['id_school'])
            
            user = User(
                username=content['username'], password=content['password'], firstname=content['firstname'],
                lastname=content['lastname'], id_school=content['id_school'], role='student'
            )
            
            content.pop('password')
            student = Student(**content)
            
            student.birth_date = isoparse(student.birth_date)
            student.age = age_from_birth_date(student.birth_date)
            
            course_ = Course.objects.get(id_school=student.id_school, code=student.course)

            user.validate()
            student.validate()

            student.save()
            user.save()
            
            school.add_student(school_, {
                'firstname': student.firstname,
                'lastname': student.lastname,
                'username': student.username,
                'photo': student.photo,
            })
            course.add_student(course_, {
                'firstname': student.firstname,
                'lastname': student.lastname,
                'username': student.username,
                'photo': student.photo,
            })
            
        except ValidationError as e:
            return {'msg': 'Invalid user data', 'err': str(e)}
        except NotUniqueError:
            return {'msg': 'Some fields required as unique are repeated'}
        except School.DoesNotExist:
            return {'msg': 'Invalid school'}
        except Course.DoesNotExist:
            return {'msg': 'Invalid course'}
        except KeyError: 
            return {'msg': 'Required fields not provided'}
        except Exception as e:
            return {'msg': 'Exception', 'err': str(e)}

        return {'msg': 'Student edited'}
    except KeyError: 
        return {'msg': 'Required fields not provided'}
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}

def put_student(username, content):
    try:
        content.pop('role', None)
        content.pop('id_school', None)
        
        user = User.objects.get(username=username)
        student = Student.objects.get(username=username)
        course_start = student.course

        user_fields = list({'username', 'password', 'firstname', 'lastname', 
            'id_school'}.intersection(content.keys()))
        user_mod = { field: content[field] for field in user_fields }
        
        content.pop('password', None)
        if content.get('birth_date', None):
            content['birth_date'] = isoparse(content['birth_date'])
            content['age'] = age_from_birth_date(content['birth_date'])
        if content.get('course', None):
            Course.objects.get(id_school=student.id_school, code=content['course'])

        done = (student.modify(**content) if content != {} else True) and (user.modify(**user_mod) if user_mod != {} else True)
        if not done: return {'msg': 'The database doesn\'t match the query'}

        school.edit_student_from_school(student.id_school, username, {
            'firstname': student.firstname,
            'lastname': student.lastname,
            'username': student.username,
            'photo': student.photo,
        })
        
        course_end = student.course
        if course_start != course_end:
            course.del_student_from_course(student.id_school, course_start, {
                'firstname': student.firstname,
                'lastname': student.lastname,
                'username': student.username,
                'photo': student.photo,
            })
            course.add_student_to_course(student.id_school, course_end, student)
        else:
            course.edit_student_from_course(student.id_school, course_start, student.username, {
                'firstname': student.firstname,
                'lastname': student.lastname,
                'username': student.username,
                'photo': student.photo,
            })

        return {'msg': 'Student edited succesfully'}
    except User.DoesNotExist:
        return {'msg': 'User does not exist'}
    except Student.DoesNotExist:
        return {'msg': 'Unexpected error'}
    except Course.DoesNotExist:
        return {'msg': 'Invalid course'}
    except NotUniqueError:
        return {'msg': 'Some fields required as unique are repeated'}
    except KeyError: 
        return {'msg': 'Required fields not provided'}
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}

def delete_student(username):
    try:
        user = User.objects.get(username=username)
        student = Student.objects.get(username=username)

        user.delete()
        student.delete()

        school.del_student_from_school(student.id_school, username)
        course.del_student_from_course(student.id_school, student.course, username)

        return {'msg': 'Student deleted succesfully'}
    except User.DoesNotExist:
        return {'msg': 'Non existing user'}
    except Student.DoesNotExist:
        return {'msg': 'Unexpected error'}
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}

# FIELDS ***********************************************

# Course
def edit_course_from_student(username, course_code):
    try:
        return edit_course(Student.objects.get(username=username), course_code)
    except Student.DoesNotExist:
        return False

def edit_course(student, course_code):
    try:
        student.course = course_code
        student.save()
        return True
    except ValidationError:
        return False

def del_course_from_student(username):
    try:
        return del_course(Student.objects.get(username=username))
    except Student.DoesNotExist:
        return False

def del_course(student):
    try:
        student.course = ''
        student.save()
        return True
    except ValidationError:
        return False

# School
def edit_id_school_from_student(username, id_school):
    try:
        return edit_id_school(Student.objects.get(username=username), id_school)
    except Student.DoesNotExist:
        return False

def edit_id_school(student, id_school):
    try:
        student.id_school = id_school
        student.save()
        return True
    except ValidationError:
        return False
