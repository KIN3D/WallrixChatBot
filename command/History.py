# Автор: Krashe85 vk:@Krashe85
from system.Command import BaseCommand
from system.answer import getInfo
from system.User import User


class HistoryCommand(BaseCommand):
    def onCommand(self):
        finalMsg = ''
        for i in self.aimed.getHistory()[:11]:
            if i['type'] == 'ban':
                banAuthor = User(id=i['byvkid'])
                finalMsg += '[B] Бан выдал {} {} \n'.format(banAuthor.getRank().getName(), banAuthor.ping())
            elif i['type'] == 'mute':
                muteAuthor = User(id=i['byvkid'])
                finalMsg += '[М] Мут выдал {} {} \n'.format(muteAuthor.getRank().getName(), muteAuthor.ping())
            elif i['type'] == 'back_list':
                blAuthor = User(id=i['byvkid'])
                finalMsg += '[L] Добавил в чс проекта {} {} \n'.format(blAuthor.getRank().getName(), blAuthor.ping())
            elif i['type'] == 'kick':
                kick = User(id=i['byvkid'])
                finalMsg += '[K] кикнул {} {} \n'.format(kick.getRank().getName(), kick.ping())
            else:
                unknow = User(id=i['byvkid'])
                finalMsg += '[K] неизвестно от {} {} \n'.format(unknow.getRank().getName(), unknow.ping())

        if not finalMsg:
            finalMsg = 'Не найдено'
        self.dialog.msg(text=getInfo("userHistory").format(self.aimed.getRank().getName(), self.aimed.ping(),
                                                           finalMsg))

