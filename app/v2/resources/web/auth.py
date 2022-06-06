from v2.models import User, Admin
from flask_jwt_extended import create_access_token
from flask import jsonify

def auth(content):
    result = {}
    try:
        user = User.objects.get(username=content['username'], password=content['password'])
        result['token'] = create_access_token({
            'username': user.username,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'role': user.role
        })
    except User.DoesNotExist:
        try:
            admin = Admin.objects.get(username=content['username'], password=content['password'])
            result['token'] = create_access_token({
                'username': admin.username,
                'firstname': admin.firstname,
                'lastname': admin.lastname,
                'role': 'admin'
            })
        except Admin.DoesNotExist:
            result['token'] = None

    return jsonify(result)
