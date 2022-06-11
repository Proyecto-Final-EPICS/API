from mongoengine import NotUniqueError, ValidationError, DoesNotExist
from flask import jsonify
from v2.models import Course, Professor, Student
from v2.common import authDecorators, find
from . import school

# get all courses of a school
# @authDecorators.school_member_required
def get_courses(id_school):
    try:
        courses = Course.objects(id_school=id_school)
        # if not courses:
        #     raise DoesNotExist('No courses found')
        return courses.to_json()
    except DoesNotExist:
        return {'msg': 'School does not exist'}

# get a course of a school
# @authDecorators.school_member_required
def get_course(id_school, course_code):
    try:
        course = Course.objects.get(id_school=id_school, code=course_code)
        # if not course:
        #     raise DoesNotExist('Course does not exist')
        return course.to_json()
    except DoesNotExist:
        return {'msg': 'School does not exist'}

# create a course of a school
@authDecorators.school_member_required
def create_course(id_school, content):
    try:
        course = Course(id_school=id_school, **content)
        course.save()
        return course.to_json()
    except NotUniqueError:
        return {'msg': 'Course already exists'}
    except ValidationError:
        return {'msg': 'Invalid course data'}

# delete a course of a school
@authDecorators.school_member_required
def delete_course(id_school, course_code):
    try:
        course = Course.objects.get(id_school=id_school, code=course_code)
        course.delete()
        school.del_course(course)
        return get_courses(course.id_school)
    except DoesNotExist:
        return {'msg': 'Course does not exist'}

# Update a course of a school
@authDecorators.school_member_required
def put_course(id_school, course_code, content):
    try:
        course = Course.objects.get(id_school=id_school, code=course_code)
        done = course.modify(**content) if content != {} else True

        if done:
            school.edit_course(course_code, course)
            return course.to_json()
        return {'msg': 'The database doesn\'t match the query'}
    except Course.DoesNotExist:
        return {'msg': 'Course does not exist'}
    except NotUniqueError:
        return {'msg': 'Some fields required as unique are repeated'}
    except KeyError:
        return {'msg': 'Required fields not provided'}

# #############################################################################
from v2.common.authDecorators import rector_or_admin_required

@rector_or_admin_required
def post_course(id_school, content):
    resp = {}
    try:
        Course.objects.get(id_school=id_school, code=content['code'])
        resp = {'msg': 'Course already exists'}, 400
    except Course.DoesNotExist:
        # course = Course(id_school=id_school, **content)
        course = Course(
            id_school=id_school, 
            code=content['code'], 
            name=content['name'], 
            period=content['period'], 
            level=content.get('level', ''), 
            capacity=content.get('capacity', ''), 
            students=content.get('students', []), 
            professors=content.get('professors', []), 
            games=content.get('games', []), 
        )
        try:
            course.validate()
            course.save()
            school.add_course(course)
            
            resp = {'msg': 'Course created successfully'}, 201
        except ValidationError:
            resp = {'msg': 'Invalid Data'}, 401
        except NotUniqueError:
            resp = {'msg': 'Not unique course'}, 401
        except Exception:
            resp = {'msg': 'Error creating course'}, 500
    except KeyError as e: 
        resp ={'msg': 'Required fields not provided', 'err': str(e)}

    return resp

# FIELDS ***********************************************

# Student
def add_student(student):
    course = Course.objects.get(id_school=student.id_school, code=student.course)
    course.students.append({
        'firstname': student.firstname,
        'lastname': student.lastname,
        'username': student.username,
    })
    course.save()

def edit_student(username, student):
    course = Course.objects.get(id_school=student.id_school, code=student.course)
    course.students[find(course.students, lambda s: s['username'] == username)] = {
        'firstname': student.firstname,
        'lastname': student.lastname,
        'username': student.username,
    }
    course.save()

# def del_student(student):
#     course = Course.objects.get(id_school=student.id_school, code=student.course)
#     course.students.pop(find(course.students, lambda s: s['username'] == student.username))
#     course.save()
    
def del_student(course_code, student):
    course = Course.objects.get(id_school=student.id_school, code=course_code)
    course.students.pop(find(course.students, lambda s: s['username'] == student.username))
    course.save()
    
# Professor
def add_professor(id_school, course_code, prof):
    try:
        course = Course.objects.get(id_school=id_school, code=course_code)
        course.professors.append({
            'firstname': prof.firstname,
            'lastname': prof.lastname,
            'username': prof.username,
            'department': prof.department,
        })
        course.save()
        return True
    except (Course.DoesNotExist, ValidationError):
        return False

def edit_professor(id_school, course_code, username, prof):
    try:
        course = Course.objects.get(id_school=id_school, code=course_code)
        course.professors[find(course.professors, lambda p: p['username'] == username)] = {
            'firstname': prof.firstname,
            'lastname': prof.lastname,
            'username': prof.username,
            'department': prof.department,
        }
        course.save()
        return True
    except (Course.DoesNotExist, ValidationError):
        return False

def del_professor(id_school, course_code, username):
    try:
        course = Course.objects.get(id_school=id_school, code=course_code)
        course.professors.pop(find(course.professors, lambda p: p['username'] == username))
        course.save()
        return True
    except (Course.DoesNotExist, ValidationError):
        return False

def update_professors(id_school, course_code):
    try:
        profs = list(filter(lambda x: (
            # course_code in map(lambda c: c['code'], x.courses)
            course_code in [c['code'] for c in x.courses]
        ), Professor.objects(id_school=id_school)))
        
        return Course.objects.get(id_school=id_school).modify(
            professors=list(map(lambda x: {
                'username': x.username,
                'firstname': x.firstname,
                'lastname': x.lastname,
                'department': x.department,
            }, profs))
        )
    except (Course.DoesNotExist, Professor.DoesNotExist):
        return False
