from flask import Blueprint, request, jsonify
import v2.resources.web.user as user

app = Blueprint('web', __name__)

@app.route('/')
def root():
    return jsonify(msg="Welcome to /v2.0/web")

# Se podría usar blueprints o resources
@app.route('/login', methods=['POST'])
def login():
    return user.login(request.get_json())

@app.route('/user', methods=['POST'])
def post_user():
    return user.post_user(request.get_json())

@app.route('/user', methods=['DELETE'])
def delete_user():
    return user.delete_user(request.get_json())

@app.route('/user', methods=['PUT'])
def put_user():
    return user.put_user(request.get_json())
