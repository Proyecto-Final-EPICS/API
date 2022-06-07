from flask_restful import Resource
from flask import request
from v1.database.commonQueries import get_registers, post_register
from v1.database.specialQueries import getSessionGamesByStudent, getGameSessionsOfStudent

class SessionGame(Resource):
    def get(self):
        return get_registers("sessionGame")
    
    def put(self):
        content = request.get_json()
        return post_register("sessionGame", content)

class SessionByStudent(Resource):
    def get(self):
        return getSessionGamesByStudent()
    def post(self):
        return getGameSessionsOfStudent()