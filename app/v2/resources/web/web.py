from flask import Blueprint, request, jsonify
from v2.models import Admin, Rector, Professor
from .auth import auth

app = Blueprint('web', __name__)

@app.route('/')
def root():
    return jsonify(msg="Welcome to /v2.0/web")

@app.route('/login', methods=['POST'])
def login():
    content = request.get_json()
    return auth(Professor, content) or auth(Rector, content) or auth(Admin, content)

@app.route('/<string:role>', methods=['POST'])
def reg_user():
    content = request.get_json()
    return ''
