from typing import List, Any, Callable, Optional
from v2.models.SessionGame import Resume
from v2.models import Game, SessionGame, School

# calcula un puntaje en base a un número de aciertos y un número de fallos
def calculate_module_score(numAciertos, numPreguntas):
    """
    Calculate the score of a module.

    :param numAciertos: The number of acerts.
    :param numPreguntas: The total number of questions.
    """
    return (numAciertos * 100) / numPreguntas

def calculate_score(resume: Resume) -> float:
    """
    Calculate the score of a resume.
    """
    numModules = len(resume.modules)
    # calculate the average score of the modules
    averageScore = 0
    for module in resume.modules:
        averageScore += module.score
    averageScore /= numModules
    
    return averageScore
    
    

def find(lst: List[Any], key: Callable[[Any], bool]) -> int:
    """
    Find the index of the first element in a list that satisfies a given condition.
    
    :param lst: The list to search.
    :param key: The condition to satisfy.

    :return: The index of the first element that satisfies the condition, or -1 if no element satisfies the condition.
    """
    for i, x in enumerate(lst):
        if key(x):
            return i
    return -1

def get_user_from_token(token: str) -> Optional[str]:
    """
    Get the user from a token.
    """
    raise NotImplementedError
from datetime import date

# https://stackoverflow.com/questions/2217488/age-from-birthdate-in-python
def age_from_birth_date(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def get_schoolId_from_schoolName(schoolName: str) -> str:
    """
    Get the schoolId from a school name.
    """
    school = School.objects.get(school_name=schoolName)
    return school.id_school


def get_num_questions_module(game: Game, module: str) -> int:
    """
    Get the number of questions of a game.

    :param game: The game.
    :param module: The module.

    :return: The number of questions.

    :raise: Exception if the module is not found.
    """
    return game.modules.get(name=module).num_questions