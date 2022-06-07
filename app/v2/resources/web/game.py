from mongoengine import NotUniqueError, ValidationError, DoesNotExist
from v2.models import Course, Game
from flask import jsonify
from v2.common.authDecorators import school_member_required

# post a game and add it to a course
@school_member_required
def post_game(id_school, code_course, content):
    try:
        course: Course = Course.objects.get(id_school=id_school, code=code_course)
        game = Game(**content)
        game.save()
        # add the game to the course games list (with mongoengine)
        course.games.append({'code': game.code, 'name': game.name})
        course.save()
        return game
    except DoesNotExist:
        return {'msg': 'Course does not exist'}
    except NotUniqueError:
        return {'msg': 'Some fields required as unique are repeated'}
    except ValidationError:
        return {'msg': 'Invalid game data'}

# get all games of a course
@school_member_required
def get_games(id_school, code_course):
    try:
        course: Course = Course.objects.get(id_school=id_school, code=code_course)
        return jsonify(course.games)
    except DoesNotExist:
        return {'msg': 'Course does not exist'}

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
        return course
    except DoesNotExist:
        return {'msg': 'Course does not exist'}
