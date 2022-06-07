from v2.models import Course, School
from v2.common.authDecorators import rector_or_admin_required
from mongoengine import ValidationError


@rector_or_admin_required
def create_course(content):
    resp = {}
    try:
        course = Course.objects.get(name=content["name"])
        if course:
            resp = {"message": "Course already exists"}, 400
    except:
        if "id_school" in content:
            # TODO: check if school exists
            try:
                course = Course(
                    code=content["code"],
                    id_school=content["id_school"],
                    name=content["name"],
                    professors=content["professors"],
                    level=content["level"],
                    period=content["period"],
                    students=content["students"],
                    games=content["games"],
                )
                course.save()
                resp = {"message": "Course created successfully"}, 201
            except ValidationError:
                resp = {"message": "Invalid Data"}, 401
            except Exception:
                resp = {"message": "Error creating course"}, 500

        else:
            resp = {"message": "Missing id_school"}, 400
    return resp
