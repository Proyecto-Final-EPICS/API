
def get_pipeline(id_school, id_game):
    return [
    {"$match": {"id_school": id_school, "game_code": id_game}},
    # project the user, game_code, id_course, sessions, and id_school
    {"$project": {
        "user": 1,
        "game_code": 1,
        "id_course": 1,
        "sessions": 1,
        "id_school": 1,
        "_id": 0
    }},
    # unwind the sessions array
    {"$unwind": "$sessions"},

    # look for a student with the username
    {
        "$lookup": {
            "from": "users",
            "localField": "user",
            "foreignField": "username",
            "as": "user_info"
        }
    },

    # project the sessions.date as startTime and endTime
    # and save the user, id_course, and id_school as an object called student
    # and save the game_code as an object called game
    # under the game, save a new array called levels with the sessions.modules.moduleId and sessions.modules.score
    # into the student save the user_info.first_name and user_info.last_name
    {"$project": {
        "startTime": "$sessions.date",
        "endTime": "$sessions.date",
        "student": {
            "username": "$user",
            "course": "$id_course",
            "school": "$id_school",
            "first_name": {"$arrayElemAt": ["$user_info.firstname", 0]},
            "last_name": {"$arrayElemAt": ["$user_info.lastname", 0]}
        },
        "games": [{
            "code": "$game_code",
            "name": "$game_code",
            "score": "$sessions.score",
            "levels": {
                "$map": {
                    "input": "$sessions.modules",
                    "as": "module",
                    "in": {
                        "level": "$$module.moduleId",
                        "score": "$$module.score",
                        "num_right_ans": 0,
                        "num_fails": 0,
                        "accuracy": "$$module.score",
                        "winLevel": "$$module.approved"
                    }
                }
            }
        }]
    }}
]