from flask import Blueprint, request, jsonify
from v2.models import User, Admin, Rector, Professor
from .auth import auth

app = Blueprint('web', __name__)

@app.route('/')
def root():
    return jsonify(msg="Welcome to /v2.0/web")

@app.route('/login', methods=['POST'])
def login():
    return auth(request.get_json())

@app.route('/register/<string:role>', methods=['POST'])
def reg_user():
    content = request.get_json()
    return ''
