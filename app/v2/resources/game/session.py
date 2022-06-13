from flask import current_app, jsonify
from v2.common import *
from v2.models import *
import mongoengine.base.datastructures as bds
from mongoengine import DoesNotExist
from typing import *

from v2.models.SessionGame import Session, SessionModule

def post_progress(content):
    # logging the content
    print(content)
    current_app.logger.info(content)
    '''
    the content is a dict with the following structure:
    {'Time': 9.100059509277344, 'Appname': 'presentacion', 'Game': {'idsesion': 0, 'idgame': '4', 'namegame': 'Frases', 
    'Totalp': 3, 'pcorrectas': 0, 'pincorrectas': 3}, 'Student': {'username': 'student4', 'school': 'Test-School'}}
    '''
    # get the game from the content
    module = content['Game']
    id_session = module['idsesion']
    # get the student from the content
    student = content['Student']
    # get the time from the content
    time = content['Time']
    # get the appname from the content
    appname = content['Appname']

    #  check the student, school and game
    game = check_request(student, appname)
    if not game:
        return jsonify({'error': 'Error in the request a'})

    # verify if the module is in the game
    try:
        game.modules.get(name=module['namegame'])
    except DoesNotExist:
        return jsonify({'error': 'Module does not exist'}), 400

    # calculate the score
    try:
        score = calculate_module_score(module['pcorrectas'], get_num_questions_module(game, module['namegame']))
    except Exception as e:
        print('error', e)
        return jsonify({'error': 'module not found'}), 404

    # get the session with student and game
    try:
        session_game = SessionGame.objects.get(user=student['username'], game_code=game.code)

        session_list: bds.EmbeddedDocumentList = session_game.sessions
        # get the session with the id_session
        try:
            session = session_list.get(id_session=id_session)
        except DoesNotExist:
            # create a new session
            session = session_list.create(id_session=id_session)
            # increment the resume numSessions
            session_game.resume.numSessions += 1

        session.time += time
        # check if a SessionModule with the module_code exists
        # otherwise create a new SessionModule
        try:
            session_module = session.modules.get(moduleId=module['namegame'])
            # update the session_module
            session_module.score = score
            session_module.time = time
            session_module.aproved = score>=60

        except DoesNotExist:
            session_module = session.modules.create(moduleId=module['namegame'], score=score, time=time, aproved=score>=60)
            

        # save the session
        # session.modules.save()

        # update the resume of the session_game
        calculate_resume(session_game.resume, session_module, game)

        # set the session score as the resume score
        session.score = session_game.resume.score

        # save the session_list
        session_list.save()
        # save the session_game
        session_game.save()

    except SessionGame.DoesNotExist:
        raise Exception('SessionGame not found, a mimir')
    except Exception as e:
        print('error', e)
        return jsonify({'error': 'error'}), 500

    return "suerte con eso"


def calculate_resume(resume: Resume, module: SessionModule, game: Game) -> None:
    # calculate the resume of the session_game
    # update the modules of the resume
    print(module)
    count_modules = game.modules.count()
    try:
        resume_module = resume.modules.get(moduleId=module.moduleId)
        # increment the time
        resume_module.time += module.time
        # set the best score
        if module.score > resume_module.score:
            resume.score += (module.score - resume_module.score)/count_modules
            resume_module.score = module.score

        # set the aproved
        if module.aproved:
            resume_module.aproved = module.aproved
    except DoesNotExist:
        # create a new resume_module
        resume_module = resume.modules.create(moduleId=module.moduleId, score=module.score, time=module.time, aproved=module.aproved)
        # increment the resume.score
        resume.score += (module.score/count_modules)

    
    # update the resume time
    resume.time += module.time


def check_request(student, appname: str) -> Optional[Game]:
    # destructuring the student
    username = student['username']
    school = student['school']

    
    # ask for the student and the game
    try:
        # get the school_id from the school_name
        id_school = get_schoolId_from_schoolName(school)

        # get the game from the game_name and the school_id
        game = Game.objects.get(name=appname, id_school=id_school)

        # if the game is 'presentacion' and the school is 'Test-School' return True
        if school == 'School_1':
            return game

        student = Student.objects.get(username=username)

        # check if the student is in the school
        if student.school_id == id_school:
            return game
        else:
            return None
            
    except DoesNotExist:
        return None
    except Exception as e:
        print('error', e)
        return None
