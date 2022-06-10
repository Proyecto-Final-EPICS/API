from v2.models import User, Admin, Student, Professor, Rector
from flask_jwt_extended import create_access_token
from flask import jsonify
from v2.common.authDecorators import role_permission_required
from mongoengine import NotUniqueError, ValidationError

def login(content):
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
        result['token'] = None

    return result

def get_users():
    return {
        # 'user': User.objects.to_json(),
        'admin': Admin.objects.to_json(),
        'rector': Rector.objects.to_json(),
        'professor': Professor.objects.to_json(),
        'student': Student.objects.to_json(),
    }
    
def get_user(username):
    try:
        user = User.objects.get(username=username)
        if user.role == 'student':
            elem = Student.objects.get(username=username)
        elif user.role == 'professor':
            elem = Professor.objects.get(username=username)
        elif user.role == 'rector':
            elem = Rector.objects.get(username=username)
        elif user.role == 'admin':
            elem = Admin.objects.get(username=username)

        return {'user': user, user.role: elem}
        
    except User.DoesNotExist:
        return {'msg': 'User does not exist'} 
    except (Student.DoesNotExist, Professor.DoesNotExist, Rector.DoesNotExist, Admin.DoesNotExist):
            return {'msg': 'Unexpected error'} 

@role_permission_required('>')
def post_user(content):
    try:
        role = content['role']
        username = content['username']

        User.objects.get(username=username)
        return {'msg': 'User already exists'}
    except User.DoesNotExist:
        password = content['password']
        firstname = content['firstname']
        lastname = content['lastname']
        id_school = content['id_school']
        identity_doc = content['identity_doc']
        birth_date = content['birth_date']
        
        user = User(
            username=username, password=password, firstname=firstname, 
            lastname=lastname, id_school=id_school, role=role
        )
        if role == 'student':
            elem = Student(
                username=username, firstname=firstname, lastname=lastname, 
                id_school=id_school, identity_doc=identity_doc, birth_date=birth_date,
                course=content['course'], doc_type=content['doc_type'],
                # phone=content['phone'], email=content['email'], legal_rep=content['legal_rep'],
            )
        elif role == 'professor':
            elem = Professor(
                username=username, firstname=firstname, lastname=lastname, 
                id_school=id_school, identity_doc=identity_doc, birth_date=birth_date,
                # phone=content['phone'], email=content['email'],
            )
        elif role == 'rector':
            elem = Rector(
                username=username, firstname=firstname, lastname=lastname, 
                id_school=id_school, identity_doc=identity_doc, birth_date=birth_date,
                # phone=content['phone'], email=content['email'],
            )
        else: return {'msg': 'User to post must be either a student, a professor or a rector'}
        
        try:
            user.validate()
            elem.validate()

            elem.save()
            user.save()
        except ValidationError:
            return {'msg': 'Invalid user data'}
        except NotUniqueError:
            return {'msg': 'Some fields required as unique are repeated'}

        return {'user': user, role: elem}
    except KeyError: return {'msg': 'Required fields not provided'}

def delete_user(username):

    @role_permission_required('>')
    def with_role(content, user):
        try:
            if(content['role'] == 'student'):
                elem = Student.objects.get(username=username)
            elif(content['role'] == 'professor'):
                elem = Professor.objects.get(username=username)
            elif(content['role'] == 'rector'):
                elem = Rector.objects.get(username=username)
            else: return {'msg': 'User to delete must be either a student, a professor or a rector'}

            user.delete()
            elem.delete()

            # return {'msg': 'Successful operation'}
            return User.objects.to_json()

        except (Student.DoesNotExist, Professor.DoesNotExist, Rector.DoesNotExist):
            return {'msg': 'Unexpected error'}

    try:
        user = User.objects.get(username=username)
        content = {'role': user.role}
        return with_role(content, user)

    except User.DoesNotExist: return {'msg': 'Non existing user'}

def put_user(username, content):

    @role_permission_required('>')
    def with_role(content, user):
        try:
            role = content['role']

            if(role == 'student'):
                elem = Student.objects.get(username=username)
            elif(role == 'professor'):
                elem = Professor.objects.get(username=username)
            elif(role == 'rector'):
                elem = Rector.objects.get(username=username)
            else: return {'msg': 'User to modify must be either a student, a professor or a rector'}

            username_mod = content['username']
            password = content['password']
            firstname = content['firstname']
            lastname = content['lastname']
            id_school = content['id_school']
            identity_doc = content['identity_doc']
            birth_date = content['birth_date']
            
            user_mod = {
                'username': username_mod, 'password': password, 'firstname': firstname, 
                'lastname': lastname, 'id_school': id_school, 'role': role
            }
            elem_mod = {
                    'username': username_mod, 'firstname': firstname, 'lastname': lastname, 
                    'id_school': id_school, 'identity_doc': identity_doc,
                    'birth_date': birth_date
                }
            if role == 'student':
                elem_mod['course'] = content['course']
                elem_mod['doc_type'] = content['doc_type']

            elif role == 'professor':
                pass
            elif role == 'rector':
                pass

            done = elem.modify(**elem_mod) and user.modify(**user_mod)
            if done: return {'user': user, role: elem}
            else: return {'msg': 'The database doesn\'t match the query'}

        except (User.DoesNotExist, Student.DoesNotExist, Professor.DoesNotExist, Rector.DoesNotExist):
            return {'msg': 'Unexpected error'}
        except NotUniqueError:
            return {'msg': 'Some fields required as unique are repeated'}

    try:
        user = User.objects.get(username=username)
        content['role'] = user.role
        return with_role(content, user)

    except User.DoesNotExist:
        return {'msg': 'User does not exist'}
