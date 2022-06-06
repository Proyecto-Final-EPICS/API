from v2.models import User, Admin
from flask_jwt_extended import create_access_token
from flask import jsonify

def auth(content):
    result = {}

    def query(collection):
        user = collection.objects.get(username=content['username'], password=content['password'])
        result['token'] = create_access_token({
            'username': user.username,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'role': user.role if collection == User else 'admin'
        })
    
    try: query(User)
    except User.DoesNotExist:
        try: query(Admin)
        except Admin.DoesNotExist: result['token'] = None

    return jsonify(result)
