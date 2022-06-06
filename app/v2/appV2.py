from flask import Blueprint
from v2.models import School, User
from .resources import game_app
from .resources.web import web_app

app = Blueprint('v2', __name__)
app.register_blueprint(game_app, url_prefix='/game')
app.register_blueprint(web_app, url_prefix='/web')

@app.route('/')
def getSchools():
    schools = School.objects()
    # print(schools.students)
    return schools.to_json()

@app.route('user/<rol>')
def getSchool(rol):
    user = User.objects.get_or_404(role=rol)
    return user.to_json()
