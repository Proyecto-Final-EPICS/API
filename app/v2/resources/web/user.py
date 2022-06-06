from v2.models import Role, User, Admin, Student, Professor, Rector
from flask_jwt_extended import create_access_token
from flask import jsonify
from v2.common.authDecorators import greater_than
from mongoengine import NotUniqueError, ValidationError

def login(content):
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

@greater_than()
def post_user(content):
    role_name = content['role']
    try:
        Role.objects.get(name=role_name)
        username = content['username']
        
        try:
            User.objects.get(username=username)
            return jsonify(msg='User already exists')
        except User.DoesNotExist:
            password = content['password']
            firstname = content['firstname']
            lastname = content['lastname']
            id_school = content['id_school']
            identity_doc = content['identity_doc']
            birth_date = content['birth_date']
            
            user = User(
                username=username, password=password, firstname=firstname, 
                lastname=lastname, id_school=id_school, role=role_name
            )
            if role_name == 'student':
                elem = Student(
                    username=username, firstname=firstname, lastname=lastname, 
                    id_school=id_school, identity_doc=identity_doc, birth_date=birth_date,
                    course=content['course'], doc_type=content['doc_type'],
                    # phone=content['phone'], email=content['email'], legal_rep=content['legal_rep'],
                )
            elif role_name == 'professor':
                elem = Professor(
                    username=username, firstname=firstname, lastname=lastname, 
                    id_school=id_school, identity_doc=identity_doc, birth_date=birth_date,
                    # phone=content['phone'], email=content['email'],
                )
            elif role_name == 'rector':
                elem = Rector(
                    username=username, firstname=firstname, lastname=lastname, 
                    id_school=id_school, identity_doc=identity_doc, birth_date=birth_date,
                    # phone=content['phone'], email=content['email'],
                )
            else: raise Role.DoesNotExist
            
            try:
                user.validate()
                elem.validate()

                elem.save()
                user.save()
            except ValidationError:
                return {'msg': 'Invalid user data'}
            except NotUniqueError:
                return {'msg': 'Some fields required as unique are repeated'}

            return {'user': user, role_name: elem}

    except Role.DoesNotExist: return jsonify(msg='Invalid role')

def delete_user():
    pass
