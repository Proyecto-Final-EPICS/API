from v2.models import SessionGame
from v2.common import get_pipeline
from flask import jsonify

def get_game_sessions(id_school, id_game):
    a = SessionGame.objects().aggregate(
        get_pipeline(id_school, id_game)
    )
    # print(list(a), id_school, id_game)
    # print(get_pipeline(id_school, id_game))
    return jsonify(list(a))