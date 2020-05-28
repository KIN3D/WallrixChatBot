# Автор: Krashe85 vk:@Krashe85
from jsons.reader import AnswerFile


def getInfo(type):
    return "[INFO] " + AnswerFile()['info'][type]


def getInfraction(type):
    return "[Модерация] " + AnswerFile()['infs'][type]


def getError(type):
    return "[ERROR] " + AnswerFile()['error'][type]


def getSpecial(type):
    return AnswerFile()[type]
