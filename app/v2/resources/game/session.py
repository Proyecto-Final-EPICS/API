from flask import current_app
from v2.common import *

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
    # get the student from the content
    student = content['Student']
    # get the time from the content
    time = content['Time']
    # get the appname from the content
    appname = content['Appname']
    # calculate the score
    score = calculate_score(module['pcorrectas'], module['pincorrectas'])
    




    return "suerte con eso"