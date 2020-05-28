# Автор: Krashe85 vk:@Krashe85
import time

from lib.db_bh import Base
from lib.vk import Vk


class DB:
    def __init__(self):
        self.db = Base()

    def getUserInfo(self, id):
        return self.db.read_record(table='vk', sample=True, value='vkid', value_is_equal=id)

    # Получаем информацию о беседе
    def getConversationInfo(self, peer):
        return self.db.read_record(table='groups_list', sample=True, value='peer', value_is_equal=int(peer))

    # Создание базового пользователя
    def createBaseUser(self, id):
        data = {
            "vkid": id,
            "nick": 'NONE',
            "rank": 0,
            "mute": 0,
            "blacklist": 0,
            "mutetime": 0,
            "bantime": 0
        }
        self.db.create_record(table='vk', value=data)

    def setNick(self, user, nick):
        if not self.getUserInfo(id=user.id):
            self.createBaseUser(id=user.id)
        value = [
            {
                "table": 'vk',
                "edit_param": 'nick',
                "edit_new_param": nick,
                "value": "vkid",
                "value_is_equal": user.id
            }
        ]
        # Отправялем запросы базе
        self.db.edit_record(value=value)

    # Мут пользователя
    def muteUser(self, user, dialog, mtime):
        if not self.getUserInfo(id=user.id):
            self.createBaseUser(id=user.id)
        # создаём времянную метку
        m_time = float(mtime)
        m_time += time.time()
        mute_list = user.getMuteList()
        mute_list.append(dialog.id)
        mute_list_db = ""
        for i in mute_list:
            mute_list_db += "{} ".format(i)
        value = [
            {
                "table": 'vk',
                "edit_param": 'mutetime',
                "edit_new_param": m_time,
                "value": "vkid",
                "value_is_equal": user.id
            },
            {
                "table": 'vk',
                "edit_param": 'muted_peerid',
                "edit_new_param": mute_list_db,
                "value": "vkid",
                "value_is_equal": user.id
            },
            {
                "table": 'vk',
                "edit_param": 'mute',
                "edit_new_param": 1,
                "value": "vkid",
                "value_is_equal": user.id
            }
        ]
        # Отправялем запросы базе
        self.db.edit_record(value=value)

    # Бан пользователя
    def banUser(self, user, dialog, btime):
        if not self.getUserInfo(id=user.id):
            self.createBaseUser(id=user.id)
        # создаём времянную метку
        b_time = float(btime)
        b_time += time.time()
        ban_list = user.getBanList()
        ban_list.append(dialog.id)
        ban_list_db = ""
        for i in ban_list:
            ban_list_db += "{} ".format(i)
        value = [
            {
                "table": 'vk',
                "edit_param": 'bantime',
                "edit_new_param": b_time,
                "value": "vkid",
                "value_is_equal": user.id
            },
            {
                "table": 'vk',
                "edit_param": 'ban_peerid',
                "edit_new_param": ban_list_db,
                "value": "vkid",
                "value_is_equal": user.id
            },
            {
                "table": 'vk',
                "edit_param": 'ban',
                "edit_new_param": 1,
                "value": "vkid",
                "value_is_equal": user.id
            }
        ]
        # Отправялем запросы базе
        self.db.edit_record(value=value)

    def unmuteUser(self, user, dialog):
        list = user.getMuteList()
        list.remove(str(dialog.id))
        final_list = ""
        mute_param = 1
        if len(list) == 0:
            mute_param = 0
        for i in list:
            final_list += "{} ".format(i)
        value = [
            {
                "table": 'vk',
                "edit_param": 'muted_peerid',
                "edit_new_param": final_list,
                "value": "vkid",
                "value_is_equal": user.id
            },
            {
                "table": 'vk',
                "edit_param": 'mute',
                "edit_new_param": mute_param,
                "value": "vkid",
                "value_is_equal": user.id
            }
        ]
        self.db.edit_record(value=value)

    # Разбан пользователя
    def unbanUser(self, user, dialog):
        list = user.getBanList()
        list.remove(str(dialog.id))
        final_list = ""
        mute_param = 1
        if len(list) == 0:
            mute_param = 0
        for i in list:
            final_list += "{} ".format(i)
        value = [
            {
                "table": 'vk',
                "edit_param": 'ban_peerid',
                "edit_new_param": final_list,
                "value": "vkid",
                "value_is_equal": user.id
            },
            {
                "table": 'vk',
                "edit_param": 'ban',
                "edit_new_param": mute_param,
                "value": "vkid",
                "value_is_equal": user.id
            }
        ]
        self.db.edit_record(value=value)

    def addBlackList(self, user):
        if not self.getUserInfo(id=user.id):
            self.createBaseUser(id=user.id)
        value = [
            {
                "table": 'vk',
                "edit_param": 'blacklist',
                "edit_new_param": 1,
                "value": "vkid",
                "value_is_equal": user.id
            }
        ]
        # Отправялем запросы базе
        self.db.edit_record(value=value)

    def setRank(self, user, RankID):
        if not self.getUserInfo(id=user.id):
            self.createBaseUser(id=user.id)
        value = [
            {
                "table": 'vk',
                "edit_param": 'rank',
                "edit_new_param": RankID,
                "value": "vkid",
                "value_is_equal": user.id
            }
        ]
        # Отправялем запросы базе
        self.db.edit_record(value=value)

    def unBlackList(self, user):
        value = [
            {
                "table": 'vk',
                "edit_param": 'blacklist',
                "edit_new_param": 0,
                "value": "vkid",
                "value_is_equal": user.id
            }
        ]
        # Отправялем запросы базе
        self.db.edit_record(value=value)

    def getUserHistory(self, id):
        return self.db.read_record(table='moder_logs', sample=True, value='vkid', value_is_equal=id)

    def createLogs(self, user, moder, type, time, reason):
        data = {
            "vkid": user.id,
            "byvkid": moder.id,
            "type": type,
            "reason": reason,
            "time": time
        }
        return self.db.create_record(table='moder_logs', value=data)

    def addGroup(self, peer, type):
        data = {
            "peer": peer,
            "type": type,
            "status": 1,
            "mode": 0
        }
        return self.db.create_record(table='groups_list', value=data)

    def getAllGroup(self):
        return self.db.read_record(table='groups_list')

    def editTypeGroup(self, dialog, newtype):
        value = [
            {
                "table": 'groups_list',
                "edit_param": 'type',
                "edit_new_param": newtype,
                "value": "peer",
                "value_is_equal": dialog.id
            }
        ]
        # Отправялем запросы базе
        self.db.edit_record(value=value)

    def editStatusGroup(self, dialog, status):
        value = [
            {
                "table": 'groups_list',
                "edit_param": 'status',
                "edit_new_param": status,
                "value": "peer",
                "value_is_equal": dialog.id
            }
        ]
        # Отправялем запросы базе
        self.db.edit_record(value=value)

    def editModeGroup(self, dialog, mode):
        value = [
            {
                "table": 'groups_list',
                "edit_param": 'mode',
                "edit_new_param": mode,
                "value": "peer",
                "value_is_equal": dialog.id
            }
        ]
        # Отправялем запросы базе
        self.db.edit_record(value=value)

    def addTextInSilenceMode(self, dialog, text):
        value = [
            {
                "table": 'groups_list',
                "edit_param": 'text',
                "edit_new_param": text,
                "value": "peer",
                "value_is_equal": dialog.id
            }
        ]
        # Отправялем запросы базе
        self.db.edit_record(value=value)

    def getMuteUsers(self):
        return self.db.read_record(table='vk', sample=True, value='mute', value_is_equal=1)

    def getBanUsers(self):
        return self.db.read_record(table='vk', sample=True, value='ban', value_is_equal=1)
