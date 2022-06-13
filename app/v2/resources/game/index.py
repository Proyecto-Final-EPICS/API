from flask import Blueprint, request, jsonify
from v2.models import Game, Student, SessionGame, School
from . import session

app = Blueprint('game', __name__)

@app.route('/login', methods=['POST'])
def logStudent():
    content = request.form
    print(content)
    username = content.get('username')
    # password = content['password']
    game_name = content.get('game')
    # get the School from the game and check if the user is in the school
    try:
        game = Game.objects.get(name=game_name)
        student = Student.objects.get(username=username)
        school = student.id_school

        # check if the student have a Session on that Game
        try:
            print()
            session = SessionGame.objects.get(user=username, game_code= game.code)
            return jsonify({'username':username, 'score':session.resume.score, 'lastlevel': '0', 'win':'False', 'id_sesion': 0})
        except SessionGame.DoesNotExist:
            # create a new Session for the student  on that game
            print('Creating a new Session for the student on that game')
            session = SessionGame(user= username, game_code= game.code, id_course=student.course, id_school=school)

            session.save()
            return jsonify({'username': username, 'score': '0', 'lastlevel': '0', 'win': 'False',  'id_sesion': 0})
    except Exception as e:
        print('error', e)
        return jsonify({'username': username, 'score': '0', 'lastlevel': '0', 'win': 'False'})
    
# get schools and send the list of schools to the client in format [{'name': 'school_name', 'code': 'school_code'}]
@app.route('/schools', methods=['GET'])
def getSchools():
    schools = School.objects.all()
    schools_list = []
    for school in schools:
        schools_list.append({'Name': school.school_name, 'code': school.id_school})
    return jsonify(schools_list)

@app.route('/session', methods=['POST', 'PUT'])
def postSession():
    return session.post_progress(request.get_json())