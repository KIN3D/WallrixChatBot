# Автор: Krashe85 vk:@Krashe85
from jsons.reader import getRankNameInId


class Rank:
    def __init__(self, user):
        self.user = user
        self.rank = user.getRankID()
        self.perms = self.commandsInRank()
        # Боженьки
        self.goods = ['396978400']

    def commandsInRank(self):
        data = {
            "бан": 6,
            "чс": 9,
            "режим": 8,
            "помощь": 0,
            "история": 2,
            "кик": 5,
            "мут": 5,
            "ник": 0,
            "объявление": 7,
            "помиловать": 9,
            "ранг": 8,
            "стафф-кик": 7,
            "разбан": 6,
            "размут": 5,
            "!кто": 0,
            "!статус": 9
        }
        perm = []
        for i in data.keys():
            if data[i] <= self.rank:
                perm.append(i)
        return perm

    # Получение название ранга пользователя
    def getName(self):
        return getRankNameInId(self)['name']

    def canPerm(self, perm):
        if perm in self.perms or self.user.id in self.goods:
            return True
        else:
            return False

    def canIgnoreSilenceMode(self):
        if self.rank >= 7 or self.user.id in self.goods:
            return True
        else:
            return False

    def canInfractionLimit(self):
        if self.rank >= 5 or self.user.id in self.goods:
            return False
        else:
            return True

    def getInfractionLimit(self):
        limit = {"5": 2,
                 "6": 12,
                 "7": 48,
                 "8": 72,
                 "9": 240,
                 "10": 99999**99}
        try:
            return limit[str(self.rank)]
        except:
            return 0

    def canIgnoreMat(self):
        if self.rank >= 7:
            return True
        else:
            return False

    def canBan(self):
        return self.canPerm("бан")

    def canBlackList(self):
        return self.canPerm("чс")

    def canEditDialogMode(self):
        return self.canPerm("режим")

    def canHelp(self):
        return self.canPerm("помощь")

    def canHistory(self):
        return self.canPerm("история")

    def canKick(self):
        return self.canPerm("кик")

    def canMute(self):
        return self.canPerm("мут")

    def canNick(self):
        return self.canPerm("ник")

    def canNotice(self):
        return self.canPerm("объявление")

    def canPardon(self):
        return self.canPerm("помиловать")

    def canRank(self):
        return self.canPerm("ранг")

    def canStaffKick(self):
        return self.canPerm("стафф-кик")

    def canRazBan(self):
        return self.canPerm("разбан")

    def canRazMute(self):
        return self.canPerm("размут")

    def canWho(self):
        return self.canPerm("!кто")

    def canEditDialogStatus(self):
        return self.canPerm("!статус")