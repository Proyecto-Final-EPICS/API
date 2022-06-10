from mongoengine import NotUniqueError, ValidationError, DoesNotExist
from v2.models import Course, Game, School
from flask import jsonify
from v2.common.authDecorators import school_member_required
from v2.common.utils import find

# post a game and add it to a course
@school_member_required
def post_game(id_school, content):
    try:
        school = School.get(id_school=id_school)
        game = Game(id_school=id_school, **content)
        game.save()
        # add the game to the School games list (with mongoengine)
        school.games.append({'code': game.code, 'name': game.name, 'sDescription': game.short_description, 'logo': game.logo})
        return game.to_json()
    except DoesNotExist:
        return jsonify({'msg': 'School does not exist'}), 404
    except NotUniqueError:
        return jsonify({'msg': 'That game already exists'}), 400
    except ValidationError:
        return jsonify({'msg': 'Invalid game data'}), 400

# get all games of a course
@school_member_required
def get_games(id_school):
    try:
        school: School = School.get(id_school=id_school)
        return jsonify(school.games)
    except DoesNotExist:
        return jsonify({'msg': 'School does not exist'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# get a game of a course
@school_member_required
def get_game(id_school, code_game):
    try:
        # course: Course = Course.objects.get(id_school=id_school, code=code_course)
        game = Game.objects.get(code=code_game, id_school=id_school)
        return game.to_json()
    except DoesNotExist:
        return jsonify({'msg': 'Course does not exist'}), 404


# delete a game from a school's course
@school_member_required
def delete_game(id_school, code_course, code_game):
    try:
        course: Course = Course.objects.get(id_school=id_school, code=code_course)
        game = Game.objects.get(code=code_game)
        game.delete()
        # remove the game from the course games list (with mongoengine)
        course.games.remove({'code': game.code, 'name': game.name})
        course.save()
        return jsonify({'msg': 'Game deleted'})
    except DoesNotExist:
        return jsonify({'msg': 'Course does not exist'}), 404

# update a game from a school's course
@school_member_required
def put_game(id_school, code_game, content):
    return jsonify({'msg': 'Not implemented'}), 501

@school_member_required
def post_game_into_course(id_school, code_course, code_game):
    try:
        course: Course = Course.objects.get(id_school=id_school, code=code_course)
        game = Game.objects.get(code=code_game)
        course.games.append({'code': game.code, 'name': game.name, 'sDescription': game.short_description, 'logo': game.logo})
        course.save()
        return jsonify({'msg': 'Game added'})
    except DoesNotExist:
        return jsonify({'msg': 'Course does not exist'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def delete_game_from_course(id_school, code_course, code_game):
    try:
        course: Course = Course.objects.get(id_school=id_school, code=code_course)
        # find the game index in the course games list
        game_index = find(course.games, lambda x: x['code'] == code_game)
        # verify that the index isn't -1
        if game_index != -1:
            # remove the game from the course games list (with mongoengine)
            course.games.pop(game_index)
            course.save()
            return jsonify({'msg': 'Game deleted'})
        else:
            return jsonify({'msg': 'Game does not exist on the course'}), 404
    except DoesNotExist:
        return jsonify({'msg': 'Course does not exist'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_games_from_course(id_school, code_course):
    try:
        course: Course = Course.objects.get(id_school=id_school, code=code_course)
        return jsonify(course.games)
    except DoesNotExist:
        return jsonify({'msg': 'Course does not exist'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def delete_games_from_course(id_school, code_course):
    try:
        course: Course = Course.objects.get(id_school=id_school, code=code_course)
        course.games = []
        course.save()
        return jsonify({'msg': 'Games deleted'})
    except DoesNotExist:
        return jsonify({'msg': 'Course does not exist'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500