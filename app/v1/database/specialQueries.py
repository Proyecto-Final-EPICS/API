from v1.database.commonQueries import get_registers
from typing import Collection
from pymongo import MongoClient
from flask import jsonify, request
from v1.database.connection import get_db


def getSchools():
    db = ""
    try:
        db = get_db()
        schools = db["schools"]
        schoolList = []
        for school in schools.find():
            schoolList.append(
                {"id": school['idSchool'], "Name": school['schoolName']})
        return jsonify(schoolList)
    finally:
        if type(db) == MongoClient:
            db.close()


def addSchoolToProfessor():
    content = request.get_json()
    prof = content['username']
    schoolName = content['schools']
    db = ""
    try:
        db = get_db()
        collection = db.professor
        collection.update(
            {'username': prof},
            {'$addToSet': {'schools': schoolName}}
        )
        return "Colegio asignado a docente con exito"
    except:
        print("Could not connect to MongoDB")
    finally:
        if type(db) == MongoClient:
            db.close()


def getProfessorSchools(username):
    db = ""
    try:
        db = get_db()
        Collection = db['professor']
        query = Collection.find(
            {'username': username},
            {'schools': 1}
        )
        List = []
        for schoolList in query:
            for schoolName in schoolList['schools']:
                List.append(schoolName)
        return jsonify(List)
    except:
        pass
    finally:
        if type(db) == MongoClient:
            db.close()


def addStudent():
    content = request.get_json()
    print(content['schoolName'])
    db = ""
    schoolName = content['schoolName']
    student = content['students']
    print(student)
    try:
        db = get_db()
        collection = db.school
        collection.update(
            {'schoolName': schoolName},
            {'$addToSet': {'students': student}}
        )
        return "Estudiante agregado correctamente"
    except:
        print("Could not connect to MongoDB")
    finally:
        if type(db) == MongoClient:
            db.close()


def getStudents():
    db = ""
    schoolName = request.args.get('nameSchool')
    try:
        db = get_db()
        schools = db["schools"]
        query = schools.find(
            {'schoolName': schoolName},
            {'students': 1}
        )
        studentList = []
        for student in query:
            for st in student['students']:
                studentList.append(st)
        if len(studentList) > 0:
            return jsonify(studentList)
        else:
            studentList.append("")
            return jsonify(studentList)
    except:
        pass
    finally:
        if type(db) == MongoClient:
            db.close()


def login():
    school = request.form.get('school')
    username = request.form.get('username')
    password = request.form.get('password')
    game = request.form.get('game')
    db = get_db()
    schools = db["schools"]
    query = schools.aggregate([
        {'$match': {'schoolName': school}},
        {'$unwind': '$students'},
        {'$match': {'$and': [
            {'students.username': username},
            {'students.password': password}
        ]}
        },
        {'$project': {'students.username': 1}}
    ])
    try:
        print({'usuario': query.next()['students']['username']})
        resultado = {}
        query2 = db['sessionGame'].find({
            '$and': [
                {'Student.username': username},
                {'Game.nameGame': game}
            ]}
        ).sort([('_id', -1)]).limit(1)
        for i in query2:
            resultado = {
                'username': str(i['Student']['username']),
                'score': str(i['Game']['score']),
                'lastlevel': str(i['Game']['levels'][-1]['level']),
                'win': i['Game']['levels'][-1]['parameters'][2]['value']
            }
        if resultado != {}:
            return resultado
        else:
            return {'username': username, 'score': '0', 'lastlevel': '0', 'win': 'False'}
    except:
        return {'username': 'error', 'score': '0', 'lastlevel': '0', 'win': 'False'}


def StudentGameList():
    db = ""
    username = request.args.get('username')
    try:
        db = get_db()
        sessions = db["sessionGame"]
        gameList = []
        query = sessions.distinct(
            'Game.nameGame', {'Student.username': username})
        for name in query:
            gameList.append(name)
        return jsonify(gameList)
    finally:
        if type(db) == MongoClient:
            db.close()


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


def getGameSessionsOfStudent():
    db = ""
    content = request.get_json()
    username = content['username']
    game = content['gameName']
    try:
        db = get_db()
        sessions = db["sessionGame"]
        sessionList = []
        query = sessions.find({
            '$and': [
                {'Student.username': username},
                {'Game.nameGame': game}
            ]}, {'_id': 0})
        for session in query:
            sessionList.append(session)
        return jsonify(sessionList)
    finally:
        if type(db) == MongoClient:
            db.close()


def getSessionGamesByGames():
    db = ""
    content = request.args.get('name')
    try:
        db = get_db()
        sessions = db["sessionGame"]
        sessionList = []
        consult = sessions.find({'Game.nameGame': content}, {'_id': 0})
        for session in consult:
            sessionList.append(session)
        return jsonify(sessionList)
    except:
        return "error"
    finally:
        if type(db) == MongoClient:
            db.close()


def getGameNameAndTopic():
    db = ""
    school = request.args.get('school')
    try:
        db = get_db()
        sessions = db["sessionGame"]
        gameList = {}
        query = sessions.aggregate([
            {'$match': {'Student.school': school}},
            {'$group': {
                '_id': 0,
                'name': {'$addToSet': {'name': '$Game.nameGame', 'topic': '$Game.topic'}}
            }}])
        gameList = query.next()
        return jsonify(gameList)
    except:
        return "error"
    finally:
        if type(db) == MongoClient:
            db.close()


def lastSessionGameOfStudent(game, username):
    db = ""
    try:
        db = get_db()
        resultado = {}
        query2 = db['sessionGame'].find({
            '$and': [
                {'Student.username': username},
                {'Game.nameGame': game}
            ]}
        ).sort([('_id', -1)]).limit(1)
        for i in query2:
            resultado = {
                'username': str(i['Student']['username']),
                'score': str(i['Game']['score']),
                'lastlevel': str(i['Game']['levels'][-1]['level']),
                'win': i['Game']['levels'][-1]['parameters'][2]['value']
            }
        if resultado != {}:
            return resultado
        else:
            return {'username': username, 'score': '0', 'lastlevel': '0', 'win': 'False'}
    except:
        return {'username': 'error', 'score': '0', 'lastlevel': '0', 'win': 'False'}
    finally:
        if type(db) == MongoClient:
            db.close()


def getGameStudentProcess():
    game = request.args.get('game')
    schoolName = request.args.get('nameSchool')
    db = ""
    try:
        db = get_db()
        schools = db["schools"]
        query = schools.find(
            {'schoolName': schoolName},
            {'students': 1}
        )
        studentList = []
        for student in query:
            for st in student['students']:
                lastGame = lastSessionGameOfStudent(game, st['username'])
                if(lastGame != "NoPlay"):
                    studentList.append(lastGame)
        return jsonify(studentList)
    except:
        return "error"


def putGameObjetives():
    content = request.get_json()
    db = ""
    schoolName = content['gameName']
    object = content['objective']
    try:
        db = get_db()
        collection = db['developedGame']
        collection.update(
            {'gameName': schoolName},
            {'$addToSet': {'objectives': object}}
        )
        return "Objetivo agregado correctamente"
    except:
        return "Could not connect to MongoDB"
    finally:
        if type(db) == MongoClient:
            db.close()


def getGameObjectives():
    db = ""
    game = request.args.get('game')
    try:
        db = get_db()
        games = db["developedGame"]
        query = games.find(
            {'gameName': game},
            {'objectives': 1}
        )
        objectiveList = []
        for objective in query:
            for ob in objective['objectives']:
                objectiveList.append(ob)
        return jsonify(objectiveList)
    except:
        return "Could not connect to MongoDB"
    finally:    
        if type(db) == MongoClient:
            db.close()

def deleteObjective():
    return "Objetivo borrado"


def getGameLevels():
    game = request.args.get('game')
    username = request.args.get('username')
    db = ""
    try:
        db = get_db()
        listLevels=[]
        query2 = db['sessionGame'].find({
            '$and': [
                {'Student.username': username},
                {'Game.nameGame': game}
            ]}
        )
        for i in query2:
            listLevels.append(i['Game']['levels'])
        return listLevels
    except:
        return "error"
    finally:
        if type(db) == MongoClient:
            db.close()
