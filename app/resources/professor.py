from flask_restful import Resource
from flask import request
from database.commonQueries import autentication, get_registers, post_register
from database.specialQueries import addSchoolToProfessor, getProfessorSchools

class Professor(Resource):
    def get(self):
        return get_registers("professor")

    def put(self):
        content = request.get_json()
        return post_register("professor", content)

    def post(self):
        content = request.get_json()
        return autentication("professor", content)

class SchoolToProfessor(Resource):
    def get(self):
        username = request.args.get('username')
        return getProfessorSchools(username)
    def put(self):
        return addSchoolToProfessor()
    