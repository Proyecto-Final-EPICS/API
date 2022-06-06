from flask import Blueprint 
from flask_restful import Api
from v1.resources.admin import Admin
from v1.resources.professor import Professor, SchoolToProfessor
from v1.resources.school import School
from v1.resources.student import Student, StudentLogin, StudentGames, LastSessionStudentGame
from v1.resources.sessionGame import SessionGame, SessionByStudent
from v1.resources.Game import Game, GameBasic, GameStudent, GameObjective, GameLevels
from v1.resources.school import BasicSchool
import os

app = Blueprint('v1', __name__)

# @app.after_request
# def after_request(response):
#     print('prueba')
#     return response

api = Api(app)

api.add_resource(Admin, '/admin')
api.add_resource(Professor, '/professor')
api.add_resource(School, '/school')
api.add_resource(Student, '/student')
api.add_resource(Game, '/detailsGame')
api.add_resource(SessionGame, '/sessionGame')
api.add_resource(BasicSchool, '/getSchools')
api.add_resource(StudentLogin, '/login')
api.add_resource(SchoolToProfessor, '/professorSchool')
api.add_resource(SessionByStudent, '/getGameSessionsByStudent')
api.add_resource(StudentGames, '/StudentGames')
api.add_resource(GameBasic, '/GameInfoBasic')
api.add_resource(GameStudent, '/GameStudentProcess')
api.add_resource(GameObjective, '/GameObjectives')
api.add_resource(GameLevels, '/GameLevels')
api.add_resource(LastSessionStudentGame, '/LastSessionStudentGame')
