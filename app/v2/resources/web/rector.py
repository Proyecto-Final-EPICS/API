from flask import jsonify
from mongoengine import NotUniqueError, ValidationError
from dateutil.parser import isoparse
from random import randrange, random
from v2.common.utils import age_from_birth_date
from v2.models import Rector, User, School
from v2.common.authDecorators import role_permission_required
from . import school

def get_school_rectors(id_school):
    return Rector.objects(id_school=id_school).to_json()

# def get_school_rector(id_school, username):
#     return Rector.objects.get(username=username).to_json()

# @role_permission_required('>')
def post_rector(content):
    try:
        User.objects.get(username=content['username'])
        return {'msg': 'User already exists'}
    except User.DoesNotExist:
        try:
            school_ = School.objects.get(id_school=content['id_school'])
            
            user = User(
                username=content['username'], password=content['password'], firstname=content['firstname'],
                lastname=content['lastname'], id_school=content['id_school'], role='rector'
            )
            
            content.pop('password')
            rec = Rector(**content)

            rec.birth_date = isoparse(rec.birth_date)
            rec.age = age_from_birth_date(rec.birth_date)
        
            user.validate()
            rec.validate()
            rec.save()
            user.save()
            
            school.add_rector(school_, {
                'firstname': rec.firstname,
                'lastname': rec.lastname,
                'username': rec.username,
                'photo': rec.photo,
            })
            return {'msg': 'Rector created'}

        except ValidationError:
            return {'msg': 'Invalid user data'}
        except NotUniqueError:
            return {'msg': 'Some fields required as unique are repeated'}
        except School.DoesNotExist:
            return {'msg': 'Invalid school'}
        except KeyError:
            return {'msg': 'Required fields not provided'}
        except Exception as e:
            return {'msg': 'Exception', 'err': str(e)}

    except KeyError:
        return {'msg': 'Required fields not provided'}
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}

def put_rector(username, content):
    try:
        content.pop('role', None)
        content.pop('id_school', None)
        
        user = User.objects.get(username=username)
        rec = Rector.objects.get(username=username)

        user_fields = list({'username', 'password', 'firstname', 'lastname', 
            'id_school'}.intersection(content.keys()))
        user_mod = { field: content[field] for field in user_fields }

        content.pop('password', None)
        if content.get('birth_date', None):
            content['birth_date'] = isoparse(content['birth_date'])
            content['age'] = age_from_birth_date(content['birth_date'])

        done = (rec.modify(**content) if content != {} else True) and (user.modify(**user_mod) if user_mod != {} else True)
        if not done: return {'msg': 'The database doesn\'t match the query'}

        school.edit_rector_from_school(rec.id_school, username, {
            'firstname': rec.firstname,
            'lastname': rec.lastname,
            'username': rec.username,
            'photo': rec.photo,
        })

        return {'msg': 'Rector edited'}

    except User.DoesNotExist:
        return {'msg': 'User does not exist'}
    except Rector.DoesNotExist:
        return {'msg': 'Unexpected error'}
    except NotUniqueError:
        return {'msg': 'Some fields required as unique are repeated'}
    except KeyError: 
        return {'msg': 'Required fields not provided'}
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}

def delete_rector(username):
    try:
        user = User.objects.get(username=username)
        rec = Rector.objects.get(username=username)

        user.delete()
        rec.delete()

        school.del_rector_from_school(rec.id_school, username)
        return {'msg': 'Rector deleted succesfully'}

    except User.DoesNotExist:
        return {'msg': 'Non existing user'}
    except Rector.DoesNotExist:
        return {'msg': 'Unexpected error'}
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}

# FIELDS
# School
def edit_id_school_from_rector(username, id_school):
    try:
        return edit_id_school(Rector.objects.get(username=username), id_school)
    except Rector.DoesNotExist:
        return False

def edit_id_school(rec, id_school):
    try:
        rec.id_school = id_school
        rec.save()
        return True
    except ValidationError:
        return False
