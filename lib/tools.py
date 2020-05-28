# Автор: Krashe85 vk:@Krashe85
from system.Conversation import Dialog
from lib.db import DB


def getInfractionTime(arg):
    time = 0
    for i in range(len(arg)):
        s = arg[i]
        if s.isalpha():
            if s.lower() == 'м':
                time = int(arg[:i]) * 60
            elif s.lower() == 'ч':
                time = int(arg[:i]) * 60 * 60
            elif s.lower() == 'д':
                time = int(arg[:i]) * 60 * 60 * 24
    if time == 0:
        return
    else:
        return time


def violationLimits(user, time):
    if user.getRank().canInfractionLimit() and time > user.getRank().getInfractionLimit() * 60:
        return True
    else:
        return False


def getReason(args):
    reason = ''
    if args:
        for i in args:
            i += ' '
            reason += i
    else:
        reason = 'Не указана'
    return reason


def getAllDialogs():
    firstDialogsList = DB().getAllGroup()
    secondDialogList = []
    for i in firstDialogsList:
        obj = {"message": {
            "peer_id": i['peer']
        }}
        secondDialogList.append(Dialog(obj))
    return secondDialogList
