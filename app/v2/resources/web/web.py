from flask import Blueprint, request, jsonify
import v2.resources.web.user as user
from v2.common.authDecorators import admin_required
from . import school

app = Blueprint('web', __name__)

@app.route('/')
def root():
    return jsonify(msg="Welcome to /v2.0/web")


# create school
@app.route('/school', methods=['POST'])
@admin_required
def school():
    pass

# get school by id
@app.route('/school/<id>', methods=['GET'])
def getSchool(id):
    school.getSchool(id)

# update school by id
@app.route('/school/<id>', methods=['PUT'])
@admin_required
def updateSchool(id):
    school.updateSchool(id)

# delete school by id
@app.route('/school/<id>', methods=['DELETE'])
@admin_required
def delSchool(id):
    school.delSchool(id)

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
