from flask_restful import Resource
from flask import request
from database.commonQueries import autentication

class Admin(Resource):
    def post(self):
        content = request.get_json()
        return autentication("admin", content)
