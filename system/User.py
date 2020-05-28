# Автор: Krashe85 vk:@Krashe85
from lib.db import DB
from lib.vk import Vk
from system.Rank import Rank


class User:
    def __init__(self, id):
        self.id = id
        self.db = DB().getUserInfo(id=self.id)
        if self.db:
            self.db = self.db[0]

    # Получение системного ника пользоватлея
    def getNick(self):
        print(self.db)
        if self.db and self.db['nick'] != 'NONE':
            return self.db['nick']
        else:
            return

    # Обновление информации
    def refreshInfo(self):
        self.db = DB().getUserInfo(id=self.id)[0]

    # Установка ника
    def setNick(self, nick):
        return DB().setNick(user=self, nick=nick)

    # Получение имени пользователя
    def getFirstName(self):
        return Vk().user_info(id=self.id)['first_name']

    # Получение Фамилии
    def getLastName(self):
        return Vk().user_info(id=self.id)['last_name']

    # Создание пинга пользователя
    def ping(self):
        if self.getNick():
            return "[id{}|{}]".format(self.id, self.getNick())
        else:
            return "[id{}|{}]".format(self.id, self.getFirstName())

    # Пинг пользователя по нику
    def pingName(self):
        return "[id{}|{}]".format(self.id, self.getFirstName())

    # Получение ID ранга пользователя
    def getRankID(self):
        if self.db:
            return int(self.db['rank'])
        else:
            return 0

    # Получем Ранг пользователя
    def getRank(self):
        return Rank(self)

    # Установаить ранг
    def setRank(self, rank):
        return DB().setRank(self, rank)

    # Список диалогов где пользователь замучен
    def getMuteList(self):
        if self.db:
            if self.db['mute'] == 1:
                return self.db['muted_peerid'].split()
            else:
                return []
        else:
            return []

    # Список диалогов где пользователь забанен
    def getBanList(self):
        if self.db:
            if self.db['ban'] == 1:
                return self.db['ban_peerid'].split()
            else:
                return []
        else:
            return []

    # Добавить в чёрный список
    def setBalckList(self):
        return DB().addBlackList(self)

    # Убрать из чёрного списка
    def delBalckList(self):
        return DB().unBlackList(self)

    # Забанен ли пользователь
    def inBlackList(self):
        if self.db:
            if self.db['blacklist'] == 1:
                return True
            else:
                return False
        else:
            return False

    # История наказаний пользователя
    def getHistory(self):
        if self.db:
            return DB().getUserHistory(id=self.id)
        else:
            return []

