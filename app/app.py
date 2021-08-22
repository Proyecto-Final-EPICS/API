from flask import Flask  # , jsonify, request, make_response
# from pymongo import MongoClient
# from bson import ObjectId
from flask_cors import CORS
# import jwt
import datetime
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.admin import Admin
from resources.professor import Professor, SchoolToProfessor
from resources.school import School
from resources.student import Student, StudentLogin, StudentGames, LastSessionStudentGame
from resources.sessionGame import SessionGame, SessionByStudent
from resources.Game import Game, GameBasic, GameStudent, GameObjective, GameLevels
from resources.school import BasicSchool
import os

app = Flask(__name__)
CORS(app)
api = Api(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
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

if __name__ == '__main__':
    port = os.getenv('PORT', 5000)
    debug = os.getenv('DEBUG', True)
    app.run(host="0.0.0.0", port=port, debug=debug)
