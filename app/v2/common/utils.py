# calcula un puntaje en base a un número de aciertos y un número de fallos
def calcScore(numAciertos, numFallos):
    numPreguntas = numAciertos + numFallos
    if numPreguntas == 0:
        return 0
    else:
        return (numAciertos / numPreguntas) * 100
        