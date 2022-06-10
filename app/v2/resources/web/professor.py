from flask import jsonify
from mongoengine import NotUniqueError, ValidationError
from dateutil.parser import isoparse
from random import randrange, random
from v2.common.utils import age_from_birt_date
from v2.models import Professor, User, School
from v2.common.authDecorators import role_permission_required

def get_school_professors(id_school):
    return Professor.objects(id_school=id_school).to_json()

def get_school_professor(id_school, username):
    return Professor.objects.get(username=username).to_json()

# @role_permission_required('>')
def post_professor(content):
    try:
        User.objects.get(username=content['username'])
        return {'msg': 'User already exists'}
    except User.DoesNotExist:
        user = User(
            username=content['username'], password=content['password'], firstname=content['firstname'],
            lastname=content['lastname'], id_school=content['id_school'], role='professor'
        )
        
        prof = Professor(
            username=content['username'], firstname=content['firstname'], lastname=content['lastname'], 
            id_school=content['id_school'], identity_doc=content['identity_doc'], 
            birth_date=isoparse(content['birth_date']), gender=content.get('gender', ''),
            phone=content.get('phone', {}), email=content.get('email', ''),
            department=content.get('department', ''), courses=content.get('courses', []),
            photo=content.get('photo', 'https://randomuser.me/api/portraits/{}men/{}.jpg'.format(
                'wo' if random() < 0.5 else '',
                randrange(0, 100)
            )),
        )
        prof.age = age_from_birt_date(prof.birth_date)
        
        # content.pop('password', None)
        # content['birth_date'] = isoparse(content['birth_date'])
        # prof = Professor(**content)
        
        try:
            user.validate()
            prof.validate()

            prof.save()
            user.save()
            
            school = School.objects.get(id_school=prof.id_school)
            school['professors'].append({
                'firstname': prof.firstname,
                'lastname': prof.lastname,
                'username': prof.username,
                'department': prof.department
            })
        except ValidationError:
            return {'msg': 'Invalid user data'}
        except NotUniqueError:
            return {'msg': 'Some fields required as unique are repeated'}
        except School.DoesNotExist:
            return {'msg': 'Unexpected error'}
        
        return jsonify(prof)
    except Professor.DoesNotExist:
        return {'msg': 'Unexpected error'}
    except KeyError:
        return {'msg': 'Required fields not provided'}

def put_professor(username, content):
    try:
        user = User.objects.get(username=username)
        prof = Professor.objects.get(username=username)

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
            content['age'] = age_from_birt_date(content['birth_date'])

        # elem_mod = {
        #     'username': content['username'], 'password': content['password'], 
        #     'firstname': content['firstname'], 'lastname': content['lastname'], 
        #     'id_school': content['id_school'], 'identity_doc': content['identity_doc'],
        #     'birth_date': isoparse(content['birth_date'])
        # }

        done = (prof.modify(**content) if content != {} else True) and (user.modify(**user_mod) if user_mod != {} else True)

        if done:
            # school = School.objects.get(id_school=prof.id_school)
            # school.modify(professors={
                
            # })
            return jsonify(prof)
        return {'msg': 'The database doesn\'t match the query'}

    except User.DoesNotExist:
        return {'msg': 'User does not exist'}
    except Professor.DoesNotExist:
        return {'msg': 'Unexpected error'}
    except NotUniqueError:
        return {'msg': 'Some fields required as unique are repeated'}
    except KeyError: 
        return {'msg': 'Required fields not provided'}

def delete_professor(username):

    try:
        user = User.objects.get(username=username)
        elem = Professor.objects.get(username=username)

        user.delete()
        elem.delete()

        return Professor.objects.to_json()

    except User.DoesNotExist: return {'msg': 'Non existing user'}
    except Professor.DoesNotExist: return {'msg': 'Unexpected error'}
