from flask import Blueprint, request, jsonify
import v2.resources.web.user as user
import v2.resources.web.school as school

app = Blueprint('web', __name__)

@app.route('/')
def root():
    return jsonify(msg="Welcome to /v2.0/web")

# USER ***********************************************
# Se podría usar blueprints o resources
@app.route('/login', methods=['POST'])
def login():
    return user.login(request.get_json())

@app.route('/user')
def get_users():
    return user.get_users()

@app.route('/user/<username>')
def get_user(username):
    return user.get_user(username)

@app.route('/user', methods=['POST'])
def post_user():
    return user.post_user(request.get_json())

@app.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    return user.delete_user(username)

@app.route('/user/<username>', methods=['PUT'])
def put_user(username):
    return user.put_user(username, request.get_json())

# SCHOOL ***********************************************
@app.route('/school')
def get_schools():
    return school.get_schools()

@app.route('/school/<school>')
def get_school(id_school):
    return school.get_school(id_school)

@app.route('/school', methods=['POST'])
def post_school():
    return school.post_school(request.get_json())

@app.route('/school/<school>', methods=['DELETE'])
def delete_school(id_school):
    return school.delete_school(id_school)

@app.route('/school/<school>', methods=['PUT'])
def put_school(id_school):
    return school.put_school(school, request.get_json())
