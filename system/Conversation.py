# Автор: Krashe85 vk:@Krashe85
from lib.vk import Vk
from lib.db import DB


class Dialog:
    def __init__(self, obj):
        self.id = obj['message']['peer_id']
        self.db = DB().getConversationInfo(peer=self.id)
        if self.db:
            self.db = self.db[0]

    # Сообщение в беседу
    def msg(self, text):
        Vk().message(peer=self.id, text=text)

    # Кик пользователя
    def kickUser(self, user):
        if Vk().kick(peer_id=self.id, user_id=user.id):
            return True
        else:
            return False

    # Обновление информации
    def refreshInfo(self):
        self.db = DB().getConversationInfo(peer=self.id)

    # Статус беседы
    def inActivate(self):
        if self.db:
            if self.db['status'] == 1:
                return True
            else:
                return False
        else:
            return False

    # Создание беседы
    def add(self, type):
        return DB().addGroup(peer=self.id, type=type)

    # Активация беседы
    def activate(self):
        return DB().editStatusGroup(self, 1)

    # Деактивация беседы
    def deactivate(self):
        return DB().editStatusGroup(self, 0)

    # Тип беседы (staff, player)
    def getType(self):
        return self.db['type']

    # Стафф беседа
    def inStaff(self):
        if self.getType() == 'staff':
            return True
        else:
            return False

    # Изменение типа беседы
    def editType(self, type):
        return DB().editTypeGroup(self, type)

    # Режим молчание
    def activateSilenceMode(self, text):
        DB().editModeGroup(self, 1)
        DB().addTextInSilenceMode(self, text)

    # Выдача текста режима молчания
    def getTextSilenceMode(self):
        return self.db['text']

    # Режим разговора
    def activateSpeakMode(self):
        DB().editModeGroup(self, 0)

    # Активирован ли режим молчания
    def inSilenceMode(self):
        if self.db:
            if self.db['mode'] == 1:
                return True
            else:
                return False
        else:
            return False

    # Забанен ли пользователь
    def inBanUser(self, user):
        if self.db:
            if user.db and user.db['ban'] == 1 and str(self.id) in user.getBanList():
                return True
            else:
                return False
        else:
            return False

    # Банем пользователя
    def banUser(self, user, time):
        return DB().banUser(user, self, time)

    # разбан пользователя
    def unBanUser(self, user):
        return DB().unbanUser(user, self)

    # Замучен ли пользователь
    def inMuteUser(self, user):
        if self.db:
            if user.db and user.db['mute'] == 1 and str(self.id) in user.getMuteList():
                return True
            else:
                return False
        else:
            return False

    # Мут пользователя
    def muteUser(self, user, time):
        return DB().muteUser(user, self, time)

    # размут пользователя
    def unMuteUser(self, user):
        return DB().unmuteUser(user, self)
