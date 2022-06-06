from v1.database.specialQueries import deleteObjective, getGameLevels, getGameNameAndTopic, getGameObjectives, getGameStudentProcess, putGameObjetives
from flask_restful import Resource
from flask import request
from v1.database.commonQueries import get_registers, post_register

class Game(Resource):
    def get(self):
        return get_registers("developedGame")
    
    def put(self):
        content = request.get_json()
        return post_register("developedGame",content)

class GameObjective(Resource):
    def put(self):
        return putGameObjetives()
    
    def get(self):
        return getGameObjectives()
    
    def delete(self):
        return deleteObjective()

class GameBasic(Resource):
    def get(self):
        return getGameNameAndTopic()

class GameStudent(Resource):
    def get(self):
        return getGameStudentProcess()

class GameLevels(Resource):
    def get(self):
        return getGameLevels()