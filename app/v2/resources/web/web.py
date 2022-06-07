from flask import Blueprint, request, jsonify
import v2.resources.web.user as user
import v2.resources.web.school as school
from . import course, game


app = Blueprint("web", __name__)


@app.route("/")
def root():
    return jsonify(msg="Welcome to /v2.0/web")


# USER ***********************************************
# Se podría usar blueprints o resources
@app.route("/login", methods=["POST"])
def login():
    return user.login(request.get_json())


@app.route("/user")
def get_users():
    return user.get_users()


@app.route("/user/<username>")
def get_user(username):
    return user.get_user(username)


@app.route("/user", methods=["POST"])
def post_user():
    return user.post_user(request.get_json())


@app.route("/user/<username>", methods=["DELETE"])
def delete_user(username):
    return user.delete_user(username)


@app.route("/user/<username>", methods=["PUT"])
def put_user(username):
    return user.put_user(username, request.get_json())


# SCHOOL ***********************************************
@app.route("/school")
def get_schools():
    return school.get_schools()

@app.route('/school/<id_school>')
def get_school(id_school):
    return school.get_school(id_school)


@app.route("/school", methods=["POST"])
def post_school():
    return school.post_school(request.get_json())

@app.route('/school/<id_school>', methods=['DELETE'])
def delete_school(id_school):
    return school.delete_school(id_school)

@app.route('/school/<id_school>', methods=['PUT'])
def put_school(id_school):
    return school.put_school(id_school, request.get_json())

# COURSE ***********************************************
@app.route('/school/<school>/course')
def get_courses(school):
    return course.get_courses(school)

@app.route('/school/<id_school>/course/<code_course>')
def get_course(id_school, code_course):
    return course.get_course(id_school, code_course)

@app.route('/school/<id_school>/course', methods=['POST'])
def post_course(id_school):
    return course.post_course(id_school, request.get_json())

@app.route('/school/<id_school>/course/<code_course>', methods=['DELETE'])
def delete_course(id_school, code_course):
    return course.delete_course(id_school, code_course)

@app.route('/school/<id_school>/course/<code_course>', methods=['PUT'])
def put_course(id_school, code_course):
    return course.put_course(id_school, code_course, request.get_json())

# GAME ***********************************************
@app.route('/school/<id_school>/course/<code_course>/game')
def get_games(id_school, code_course):
    return game.get_games(id_school, code_course)

@app.route('/school/<id_school>/course/<code_course>/game/<code_game>')
def get_game(id_school, code_course, code_game):
    return game.get_game(id_school, code_course, code_game)

@app.route('/school/<id_school>/course/<code_course>/game', methods=['POST'])
def post_game(id_school, code_course):
    return game.post_game(id_school, code_course, request.get_json())

@app.route('/school/<id_school>/course/<code_course>/game/<code_game>', methods=['DELETE'])
def delete_game(id_school, code_course, code_game):
    return game.delete_game(id_school, code_course, code_game)

@app.route('/school/<id_school>/course/<code_course>/game/<code_game>', methods=['PUT'])
def put_game(id_school, code_course, code_game):
    return game.put_game(id_school, code_course, code_game, request.get_json())
    
