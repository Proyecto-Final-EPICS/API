from flask_restful import Resource
from flask import request
from database.commonQueries import get_registers, post_register
from database.specialQueries import getStudents, lastSessionGameOfStudent, login, addStudent, StudentGameList

class Student(Resource):
    def get(self):
        return getStudents()
    
    def put(self):
        content = request.get_json()
        return addStudent()

class StudentLogin(Resource):
    def post(self):
        return login()

class StudentGames(Resource):
    def get(self):
        return StudentGameList()

class LastSessionStudentGame(Resource):
    def get(self):
        game = request.args.get('game')
        username = request.args.get('username')
        return lastSessionGameOfStudent(game, username)