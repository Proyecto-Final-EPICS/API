from mongoengine import NotUniqueError, ValidationError, DoesNotExist
from flask import jsonify
from v2.models import Course
from v2.common import authDecorators

# get all courses of a school
@authDecorators.school_member_required
def get_courses(id_school):
    try:
        courses = Course.objects(id_school=id_school)
        if not courses:
            raise DoesNotExist("No courses found")
        return courses.to_json()
    except DoesNotExist:
        return {'msg': 'School does not exist'}

# get a course of a school
@authDecorators.school_member_required
def get_course(id_school, code_course):
    try:
        course = Course.objects.get(id_school=id_school, code=code_course)
        if course:
            return course.to_json()
        else:
            raise DoesNotExist("Course does not exist")
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
def delete_course(id_school, code_course):
    try:
        course = Course.objects.get(id_school=id_school, code=code_course)
        course.delete()
        return {'msg': 'Course deleted'}
    except DoesNotExist:
        return {'msg': 'Course does not exist'}

# Update a course of a school
@authDecorators.school_member_required
def put_course(id_school, code_course, content):
    return jsonify({'msg': 'Not implemented'})


# #############################################################################
from v2.common.authDecorators import rector_or_admin_required

@rector_or_admin_required
def post_course(id_school, content):
    resp = {}
    try:
        course = Course.objects.get(id_school= id_school, code=content["code"])
        if course:
            resp = {"message": "Course already exists"}, 400
    except:
        try:
            course = Course(id_school = id_school,**content)
            course.save()
            resp = {"message": "Course created successfully"}, 201
        except ValidationError:
            resp = {"message": "Invalid Data"}, 401
        except Exception:
            resp = {"message": "Error creating course"}, 500

    return resp
