from mongoengine import NotUniqueError, ValidationError, DoesNotExist
from v2.models import Course, Game, School
from flask import jsonify
from v2.common.authDecorators import school_member_required
from v2.common.utils import find
from . import course, school

# get all games of a course
# @school_member_required
def get_school_games(id_school):
    try:
        # return School.objects.get(id_school=id_school).games.to_json()
        return Game.objects(id_school=id_school).to_json()
    except Exception as e:
        return {'error': str(e)}, 500

# get a game of a course
# @school_member_required
def get_school_game(id_school, game_code):
    try:
        return Game.objects.get(code=game_code, id_school=id_school).to_json()
    except Game.DoesNotExist:
        return {'msg': 'Game does not exist'}, 404

# post a game and add it to a course
# @school_member_required
def post_game(id_school, content):
    try:
        Game.objects.get(id_school=id_school, code=content['code'])
        return {'msg': 'Game already exists'}, 400
    except Game.DoesNotExist:
        try:
            school_ = School.objects.get(id_school=id_school)
            game = Game(**content)

            game.validate()
            game.save()
            # add the game to the School games list (with mongoengine)
            school.add_game(school_, {
                'code': game.code, 'name': game.name, 'short_description': game.short_description, 
                'logo': game.logo, 'devs': game.devs, 'topic': game.topic
            })
            
            return {'msg': 'Course created successfully'}, 201
        except NotUniqueError:
            return {'msg': 'That game already exists'}, 400
        except ValidationError:
            return {'msg': 'Invalid game data'}, 400
        except School.DoesNotExist:
            return {'msg': 'Invalid school'}, 404
        except Exception as e:
            return {'msg': 'Exception', 'err': str(e)}, 500
            
    except KeyError as e: 
        return {'msg': 'Required fields not provided', 'err': str(e)}
    # except Exception as e:
    #     return {'msg': 'Exception', 'err': str(e)}, 500

# update a game from a school's course
@school_member_required
def put_game(id_school, game_code, content):
    try:
        content.pop('id_school', None)

        game = Game.objects.get(id_school=id_school, code=game_code)
        done = game.modify(**content) if content != {} else True
        if not done: return {'msg': 'The database doesn\'t match the query'}

        game_ref = {
            'code': game.code, 'name': game.name, 'short_description': game.short_description, 
            'logo': game.logo, 'devs': game.devs, 'topic': game.topic
        }
        school.edit_game_from_school(id_school, game_code, game_ref)
        courses = Course.objects(id_school=id_school)
        for course_ in courses:
            course.edit_game(course_, game_code, game_ref)
        return {'msg': 'Game edited successfully'}, 201
        
    except Game.DoesNotExist:
        return {'msg': 'Game does not exist'}
    except NotUniqueError:
        return {'msg': 'Some fields required as unique are repeated'}
    except KeyError:
        return {'msg': 'Required fields not provided'}
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}

@school_member_required
def delete_game(id_school, game_code):
    try:
        game = Game.objects.get(id_school=id_school, code=game_code)
        game.delete()
        
        school.del_game_from_school(id_school, game_code)
        courses = Course.objects(id_school=id_school)
        for course_ in courses:
            course.del_game(course_, game_code)
        
        return {'msg': 'Game deleted'}
    except Game.DoesNotExist:
        return {'msg': 'Game does not exist'}, 404
    except Exception as e:
        return {'msg': 'Exception', 'err': str(e)}

# delete a game from a school's course
@school_member_required
def delete_game_from_course(id_school, code_course, game_code):
    try:
        course: Course = Course.objects.get(id_school=id_school, code=code_course)
        game = Game.objects.get(code=game_code)
        game.delete()
        # remove the game from the course games list (with mongoengine)
        course.games.remove({'code': game.code, 'name': game.name})
        course.save()
        return jsonify({'msg': 'Game deleted'})
    except DoesNotExist:
        return jsonify({'msg': 'Game does not exist'}), 404

@school_member_required
def post_game_into_course(id_school, code_course, game_code):
    try:
        course: Course = Course.objects.get(id_school=id_school, code=code_course)
        game = Game.objects.get(code=game_code)
        course.games.append({'code': game.code, 'name': game.name, 'sDescription': game.short_description, 'logo': game.logo})
        course.save()
        return jsonify({'msg': 'Game added'})
    except DoesNotExist:
        return jsonify({'msg': 'Game does not exist'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def delete_game_from_course(id_school, code_course, game_code):
    try:
        course: Course = Course.objects.get(id_school=id_school, code=code_course)
        # find the game index in the course games list
        game_index = find(course.games, lambda x: x['code'] == game_code)
        # verify that the index isn't -1
        if game_index != -1:
            # remove the game from the course games list (with mongoengine)
            course.games.pop(game_index)
            course.save()
            return jsonify({'msg': 'Game deleted'})
        else:
            return jsonify({'msg': 'Game does not exist on the course'}), 404
    except DoesNotExist:
        return jsonify({'msg': 'Game does not exist'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_games_from_course(id_school, code_course):
    try:
        course: Course = Course.objects.get(id_school=id_school, code=code_course)
        return jsonify(course.games)
    except DoesNotExist:
        return jsonify({'msg': 'Game does not exist'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def delete_games_from_course(id_school, code_course):
    try:
        course: Course = Course.objects.get(id_school=id_school, code=code_course)
        course.games = []
        course.save()
        return jsonify({'msg': 'Games deleted'})
    except DoesNotExist:
        return jsonify({'msg': 'Game does not exist'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# School
def edit_id_school(id_school, game_code, id_school_new):
    try:
        game = Game.objects.get(id_school=id_school, game=game_code)
        game.id_school = id_school_new
        game.save()
        return True
    except (Game.DoesNotExist, ValidationError):
        return False
