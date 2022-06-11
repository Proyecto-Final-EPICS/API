from flask import jsonify
from mongoengine import NotUniqueError, ValidationError
from dateutil.parser import isoparse
from random import randrange, random
from v2.common.utils import age_from_birth_date
from v2.models import Professor, User, School, Course
from v2.common.authDecorators import role_permission_required
from . import school, course

def get_school_professors(id_school):
    return Professor.objects(id_school=id_school).to_json()

# def get_school_professor(id_school, username):
#     return Professor.objects.get(username=username)

# @role_permission_required('>')
def post_professor(content):
    try:
        User.objects.get(username=content['username'])
        return {'msg': 'User already exists'}
    except User.DoesNotExist:

        School.objects.get(id_school=content['id_school'])
        
        user = User(
            username=content['username'], password=content['password'], firstname=content['firstname'],
            lastname=content['lastname'], id_school=content['id_school'], role='professor'
        )
        
        prof = Professor(
            username=content['username'], firstname=content['firstname'], lastname=content['lastname'], 
            id_school=content['id_school'], identity_doc=content['identity_doc'], 
            birth_date=isoparse(content['birth_date']), gender=content.get('gender', ''),
            phone=content.get('phone', {}), email=content.get('email', ''),
            photo=content.get('photo', 'https://randomuser.me/api/portraits/{}men/{}.jpg'.format(
                'wo' if random() < 0.5 else '',
                randrange(0, 100)
            )),
            department=content.get('department', ''),
        )
        prof.age = age_from_birth_date(prof.birth_date)
        if content.get('courses', None):
            def get_course(course_code):
                course = Course.objects.get(id_school=prof.id_school, code=course_code)
                return {'code': course.code, 'name': course.name}
            prof.courses = list(map(get_course, content['courses']))

        try:
            user.validate()
            prof.validate()

            prof.save()
            user.save()
            
            school.add_professor(prof.id_school, prof)
            # school.update_professors(prof.id_school)
            
            for course_ in prof.courses:
                course.add_professor(prof.id_school, course_['code'], prof)
            # for course in prof.courses:
            #     course.update_professors(prof.id_school, course['code'])

        except ValidationError:
            return {'msg': 'Invalid user data'}
        except NotUniqueError:
            return {'msg': 'Some fields required as unique are repeated'}
        except School.DoesNotExist:
            return {'msg': 'Invalid school'}
        except Course.DoesNotExist:
            return {'msg': 'Invalid course(s)'}
        
        return jsonify(prof)
    except Professor.DoesNotExist:
        return {'msg': 'Unexpected error'}
    except KeyError:
        return {'msg': 'Required fields not provided'}

def put_professor(username, content):
    try:
        content.pop('role', None)
        content.pop('id_school', None)

        user = User.objects.get(username=username)
        prof = Professor.objects.get(username=username)
        courses_start = set([course['code'] for course in prof.courses])

        user_fields = list({'username', 'password', 'firstname', 'lastname', 
            'id_school'}.intersection(content.keys()))
        user_mod = { field: content[field] for field in user_fields }
        
        content.pop('password', None)
        if content.get('birth_date', None):
            content['birth_date'] = isoparse(content['birth_date'])
            content['age'] = age_from_birth_date(content['birth_date'])
        if content.get('courses', None):
            def get_course(course_code):
                course = Course.objects.get(id_school=prof.id_school, code=course_code)
                return {'code': course.code, 'name': course.name}
            content['courses'] = list(map(get_course, content['courses']))

        done = (prof.modify(**content) if content != {} else True) and (user.modify(**user_mod) if user_mod != {} else True)

        if done:
            school.edit_professor(prof.id_school, username, prof)
            # school.update_professors(prof.id_school)
            if content.get('courses', None) != None:
                courses_end = set([course['code'] for course in prof.courses])

                # print(list(courses_start.difference(courses_end)))
                for course_ in list(courses_start.difference(courses_end)):
                    course.del_professor(prof.id_school, course_, prof.username)
                
                # print(list(courses_end.difference(courses_start)))
                for course_ in list(courses_end.difference(courses_start)):
                    course.add_professor(prof.id_school, course_, prof)

                # print(list(courses_end.intersection(courses_start)))
                for course_ in list(courses_end.intersection(courses_start)):
                    course.edit_professor(prof.id_school, course_, prof.username, prof)
                
            return jsonify(prof)
        return {'msg': 'The database doesn\'t match the query'}

    except User.DoesNotExist:
        return {'msg': 'User does not exist'}
    except Professor.DoesNotExist:
        return {'msg': 'Unexpected error'}
    except Course.DoesNotExist:
        return {'msg': 'Invalid course'}
    except NotUniqueError:
        return {'msg': 'Some fields required as unique are repeated'}
    except KeyError: 
        return {'msg': 'Required fields not provided'}

def delete_professor(username):
    try:
        user = User.objects.get(username=username)
        prof = Professor.objects.get(username=username)

        user.delete()
        prof.delete()

        school.del_professor(prof.id_school, username)
        # school.update_professors(prof.id_school)
        for course_ in prof.courses:
            course.del_professor(prof.id_school, course_['code'], username)
        return get_school_professors(prof.id_school)

    except User.DoesNotExist: return {'msg': 'Non existing user'}
    except Professor.DoesNotExist: return {'msg': 'Unexpected error'}
