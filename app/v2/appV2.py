from flask import Blueprint
from v2.models import School

app = Blueprint('v2', __name__)

@app.route('/')
def getSchools():
    schools = School.objects()
    # print(schools.students)
    return schools.to_json()
