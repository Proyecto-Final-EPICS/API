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
def post_course(id_school, content):
    try:
        course = Course(id_school=id_school, **content)
        course.save()
        return course.to_json()
    except NotUniqueError:
        return {'msg': 'Course already exists'}

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