from flask import jsonify
from mongoengine import NotUniqueError, ValidationError
from dateutil.parser import isoparse
from random import randrange, random
from v2.common.utils import age_from_birth_date, find
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
        try:
            school_ = School.objects.get(id_school=content['id_school'])
            
            user = User(
                username=content['username'], password=content['password'], 
                firstname=content['firstname'], lastname=content['lastname'], 
                id_school=content['id_school'], role='professor'
            )

            content.pop('password')
            prof = Professor(**content)

            prof.birth_date = isoparse(prof.birth_date)
            prof.age = age_from_birth_date(prof.birth_date)
            if content.get('courses', None):
                def get_course(course_code):
                    course = Course.objects.get(id_school=prof.id_school, code=course_code)
                    return {'code': course.code, 'name': course.name}
                prof.courses = list(map(get_course, content['courses']))

            user.validate()
            prof.validate()
            prof.save()
            user.save()
            
            school.add_professor(school_, {
                'firstname': prof.firstname,
                'lastname': prof.lastname,
                'username': prof.username,
                'department': prof.department,
                'photo': prof.photo,
            })
            for course_ in prof.courses:
                course.add_professor_to_course(prof.id_school, course_['code'], {
                    'firstname': prof.firstname,
                    'lastname': prof.lastname,
                    'username': prof.username,
                    'photo': prof.photo,
                })
            
            return {'msg': 'Professor created successfully'}, 201
        except ValidationError:
            return {'msg': 'Invalid user data'}
        except NotUniqueError:
            return {'msg': 'Some fields required as unique are repeated'}
        except School.DoesNotExist:
            return {'msg': 'Invalid school'}
        except Course.DoesNotExist:
            return {'msg': 'Invalid course(s)'}
        except KeyError:
            return {'msg': 'Required fields not provided'}
        except Exception as e:
            return {'msg': 'Exception', 'err': str(e)}
                
    except KeyError:
        return {'msg': 'Required fields not provided'}
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}

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
        if not done: return {'msg': 'The database doesn\'t match the query'}

        school.edit_professor_from_school(prof.id_school, username, {
            'firstname': prof.firstname,
            'lastname': prof.lastname,
            'username': prof.username,
            'department': prof.department,
            'photo': prof.photo,
        })
        
        prof_course = {
            'firstname': prof.firstname,
            'lastname': prof.lastname,
            'username': prof.username,
            'photo': prof.photo,
        }
        if content.get('courses', None) != None:
            courses_end = set([course['code'] for course in prof.courses])

            for course_ in list(courses_start.difference(courses_end)):
                course.del_professor_from_course(prof.id_school, course_, prof.username)
            
            for course_ in list(courses_end.difference(courses_start)):
                course.add_professor_to_course(prof.id_school, course_, prof_course)

            for course_ in list(courses_end.intersection(courses_start)):
                course.edit_professor_from_course(prof.id_school, course_, prof.username, prof_course)
        else:
            for course_ in prof.courses:
                course.edit_professor_from_course(prof.id_school, course_['code'], prof.username, prof_course)
        
        return {'msg': 'Professor edited'}

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
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}

def delete_professor(username):
    try:
        user = User.objects.get(username=username)
        prof = Professor.objects.get(username=username)

        user.delete()
        prof.delete()

        school.del_professor_from_school(prof.id_school, username)
        
        for course_ in prof.courses:
            course.del_professor_from_course(prof.id_school, course_['code'], username)
        return {'msg': 'Professor deleted'}

    except User.DoesNotExist:
        return {'msg': 'Non existing user'}
    except Professor.DoesNotExist:
        return {'msg': 'Unexpected error'}
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}

# FIELDS ***********************************************

# Course
# def add_course(username, course):
#     try:
#         prof = Professor.objects.get(username=username)
#         prof.courses.append({
#             'code': course.code,
#             'name': course.name,
#         })
#         prof.save()
#         return True
#     except (Professor.DoesNotExist, ValidationError):
#         return False

def edit_course_from_professor(username, course_code, course):
    try:
        return edit_course(Professor.objects.get(username=username), course_code, course)
    except Professor.DoesNotExist:
        return False

def edit_course(prof, course_code, course):
    try:
        i = find(prof.courses, lambda p: p['code'] == course_code)
        if i == -1: return False

        prof.courses[i] = course
        prof.save()
        return True
    except ValidationError:
        return False

def del_course_from_professor(username, course_code):
    try:
        return del_course(Professor.objects.get(username=username), course_code)
    except Professor.DoesNotExist:
        return False

def del_course(prof, course_code):
    try:
        i = find(prof.courses, lambda p: p['code'] == course_code)
        if i == -1: return False

        prof.courses.pop(i)
        prof.save()
        return True
    except ValidationError:
        return False

# School
def edit_id_school_from_professor(username, id_school):
    try:
        return edit_id_school(Professor.objects.get(username=username), id_school)
    except Professor.DoesNotExist:
        return False

def edit_id_school(prof, id_school):
    try:
        prof.id_school = id_school
        prof.save()
        return True
    except ValidationError:
        return False
