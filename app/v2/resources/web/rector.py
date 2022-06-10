from v2.models import Rector, User
from flask import jsonify
from v2.common.authDecorators import role_permission_required
from mongoengine import NotUniqueError, ValidationError
from dateutil.parser import isoparse
from random import randrange, random

def get_school_rectors(id_school):
    return Rector.objects(id_school=id_school).to_json()

def get_school_rector(id_school, username):
    return

# @role_permission_required('>')
def post_rector(content):
    try:
        User.objects.get(username=content['username'])
        return {'msg': 'User already exists'}
    except User.DoesNotExist:
        user = User(
            username=content['username'], password=content['password'], firstname=content['firstname'],
            lastname=content['lastname'], id_school=content['id_school'], role='rector'
        )
        
        prof = Rector(
            username=content['username'], firstname=content['firstname'], lastname=content['lastname'], 
            id_school=content['id_school'], identity_doc=content['identity_doc'], 
            birth_date=isoparse(content['birth_date']),
            phone=content.get('phone', {}), email=content.get('email', ''),
            gender=content.get('gender', ''), age=content.get('age', 0), 
            photo=content.get('photo', 'https://randomuser.me/api/portraits/{}men/{}.jpg'.format(
                'wo' if random() < 0.5 else '',
                randrange(0, 100)
            )), 
            department=content.get('department', ''), 
            courses=content.get('courses', []),
        )
        
        # content.pop('password', None)
        # content['birth_date'] = isoparse(content['birth_date'])
        # prof = Rector(**content)
        
        try:
            user.validate()
            prof.validate()

            prof.save()
            user.save()
        except ValidationError as e:
            return {'msg': 'Invalid user data', 'err': str(e)}
        except NotUniqueError:
            return {'msg': 'Some fields required as unique are repeated'}

        return jsonify(prof)
    except KeyError: return {'msg': 'Required fields not provided'}

def put_rector(username, content):
    try:
        print(username)
        user = User.objects.get(username=username)
        prof = Rector.objects.get(username=username)

        user_fields = list({'username', 'password', 'firstname', 'lastname', 
            'id_school'}.intersection(content.keys()))

        user_mod = { field: content[field] for field in user_fields }

        # user_mod = {
        #     'username': content['username'], 'password': content['password'], 
        #     'firstname': content['firstname'], 'lastname': content['lastname'], 
        #     'id_school': content['id_school'],
        # }
        
        content.pop('password', None)

        if content.get('birth_date', None):
            content['birth_date'] = isoparse(content['birth_date'])

        # elem_mod = {
        #     'username': content['username'], 'password': content['password'], 
        #     'firstname': content['firstname'], 'lastname': content['lastname'], 
        #     'id_school': content['id_school'], 'identity_doc': content['identity_doc'],
        #     'birth_date': isoparse(content['birth_date'])
        # }

        done = (prof.modify(**content) if content != {} else True) and (user.modify(**user_mod) if user_mod != {} else True)

        if done: return jsonify(prof)
        return {'msg': 'The database doesn\'t match the query'}

    except User.DoesNotExist:
        return {'msg': 'User does not exist'}
    except Rector.DoesNotExist:
        return {'msg': 'Unexpected error'}
    except NotUniqueError:
        return {'msg': 'Some fields required as unique are repeated'}
    except KeyError: 
        return {'msg': 'Required fields not provided'}

def delete_rector(username):

    try:
        user = User.objects.get(username=username)
        elem = Rector.objects.get(username=username)

        user.delete()
        elem.delete()

        return Rector.objects.to_json()

    except User.DoesNotExist: return {'msg': 'Non existing user'}
    except Rector.DoesNotExist: return {'msg': 'Unexpected error'}
