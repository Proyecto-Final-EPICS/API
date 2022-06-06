from flask import Blueprint, request, jsonify
from v2.models import Game, Student, SessionGame

app = Blueprint('game', __name__)

@app.route('/login', methods=['POST'])
def logStudent():
    content = request.get_json()
    username = content['username']
    # password = content['password']
    game_name = content['game']
    # get the School from the game and check if the user is in the school
    try:
        game = Game.objects.get(name=game_name)
        school = game.id_school
        student = Student.objects.get(username=username, id_school=school)

        # check if the student have a Session on that Game
        try:
            print()
            session = SessionGame.objects.get(user=username, game_code= game.code)
            return jsonify({'username':username, 'score':session.resume.score, 'lastlevel': '0', 'win':'False'})
        except SessionGame.DoesNotExist:
            # create a new Session for the student  on that game
            print('Creating a new Session for the student on that game')
            session = SessionGame(user= username, game_code= game.code, id_course=student.course, id_school=school)
            session.save()
            return jsonify(msg="You are now logged in on this game!")
    except Exception as e:
        print('error', e)
        return jsonify({'username': username, 'score': '0', 'lastlevel': '0', 'win': 'False'})
    