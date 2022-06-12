from flask import jsonify
from mongoengine import NotUniqueError, ValidationError
from dateutil.parser import isoparse
from random import randrange, random
from v2.common.utils import age_from_birth_date
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
        School.objects.get(id_school=content['id_school'])
        
        user = User(
            username=content['username'], password=content['password'], firstname=content['firstname'],
            lastname=content['lastname'], id_school=content['id_school'], role='student'
        )
        
        student = Student(
            username=content['username'], firstname=content['firstname'], lastname=content['lastname'], 
            id_school=content['id_school'], identity_doc=content['identity_doc'], 
            birth_date=isoparse(content['birth_date']), gender=content.get('gender', ''),
            phone=content.get('phone', {}), email=content.get('email', ''),
            photo=content.get('photo', 'https://randomuser.me/api/portraits/{}men/{}.jpg'.format(
                'wo' if random() < 0.5 else '',
                randrange(0, 100)
            )),
            doc_type=content.get('doc_type', ''),
            address=content.get('address', ''), 
            legal_rep=content.get('legal_rep', Student.Representative())
        )
        student.age = age_from_birth_date(student.birth_date)
        if content.get('course', None):
            c = Course.objects.get(id_school=student.id_school, code=content['course'])
            student.course = {'code': c.code, 'name': c.name}

        try:
            user.validate()
            student.validate()

            student.save()
            user.save()
            
            school.add_student(student.id_school, student)
            course.add_student(student.id_school, student.course['code'], student)
            # course.add_student(student)
        except ValidationError:
            return {'msg': 'Invalid user data'}
        except NotUniqueError:
            return {'msg': 'Some fields required as unique are repeated'}
        except School.DoesNotExist:
            return {'msg': 'Invalid school'}
        except Course.DoesNotExist:
            return {'msg': 'Invalid course'}
        
        return jsonify(student)
    except Student.DoesNotExist:
        return {'msg': 'Unexpected error'}
    except KeyError:
        return {'msg': 'Required fields not provided'}

def put_student(username, content):
    try:
        user = User.objects.get(username=username)
        student = Student.objects.get(username=username)
        course_start = student.course['code']

        user_fields = list({'username', 'password', 'firstname', 'lastname', 
            'id_school'}.intersection(content.keys()))
        user_mod = { field: content[field] for field in user_fields }
        
        content.pop('password', None)
        if content.get('birth_date', None):
            content['birth_date'] = isoparse(content['birth_date'])
            content['age'] = age_from_birth_date(content['birth_date'])
        if content.get('course', None):
            c = Course.objects.get(id_school=student.id_school, code=content['course'])
            content['course'] = {'code': c.code, 'name': c.name}

        done = (student.modify(**content) if content != {} else True) and (user.modify(**user_mod) if user_mod != {} else True)

        if done:
            school.edit_student(student.id_school, username, student)
            
            if content.get('course', None) != None:
                course_end = student.course['code']
                if course_start != course_end:
                    course.add_student(student.id_school, course_end, student)
                    course.del_student(student.id_school, course_start, student.username)
                else:
                    course.edit_student(student.id_school, course_end, student.username, student)
            
            return jsonify(student)
        return {'msg': 'The database doesn\'t match the query'}

    except User.DoesNotExist:
        return {'msg': 'User does not exist'}
    except Student.DoesNotExist:
        return {'msg': 'Unexpected error'}
    except NotUniqueError:
        return {'msg': 'Some fields required as unique are repeated'}
    except KeyError: 
        return {'msg': 'Required fields not provided'}

def delete_student(username):
    try:
        user = User.objects.get(username=username)
        student = Student.objects.get(username=username)

        user.delete()
        student.delete()

        school.del_student(student.id_school, username)
        course.del_student(student.id_school, student.course['code'], username)

        return get_school_students(student.id_school)

    except User.DoesNotExist: return {'msg': 'Non existing user'}
    except Student.DoesNotExist: return {'msg': 'Unexpected error'}
