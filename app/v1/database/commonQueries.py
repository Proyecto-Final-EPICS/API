from pymongo import MongoClient
from flask import jsonify, request
from v1.database.connection import get_db
from flask_jwt_extended import create_access_token
from datetime import datetime

def get_registers(colection_name):
    db = ""
    try:
        db = get_db()
        colection = db[colection_name]
        registers = []
        for register in colection.find():
            register['_id'] = str(register['_id'])
            registers.append(register)
        return jsonify(registers)
    except:
        return "error de conexión al servidor bd"
    finally:
        if type(db) == MongoClient:
            db.close()

#@app.route('/getSessionGamesByStudent', methods=['GET'])
def getSessionGamesByStudent():
    db = ""
    username = request.args.get('username')
    try:
        db = get_db()
        sessions = db["sessionGame"]
        sessionList = []
        consult = sessions.find({'Student.username': username}, {'_id': 0})
        for session in consult:
            sessionList.append(session)
        return jsonify(sessionList)
    finally:
        if type(db) == MongoClient:
            db.close()

def post_register(colection_name, document):
    db = ""
    try:
        db = get_db()
        collection = db[colection_name]
        collection.insert(document)
        return "Registro exitoso"
    except:
        return "error de conexión al servidor bd"
    finally:
        if type(db) == MongoClient:
            db.close()

def autentication(colection_name, data):
    username = data["username"]
    password = data["password"]
    db = get_db()
    collection = db[colection_name]

    query = collection.aggregate([{'$match': {'$and': [
        {'username': username},
        {'password': password}
    ]}
    }])
    try:
        query.next()
        access_token = create_access_token({'user':username})
        return jsonify({'token':access_token})
    except:
        return jsonify({'token': 'none'})
        # return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
