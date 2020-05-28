# Автор: Krashe85 vk:@Krashe85
from system.User import User
from system.answer import getError


class BaseCommand:
    # Базовая структура команды
    def __init__(self, sender, dialog, errorMsgType, senderCanPerm, obj, canGetAimed=True):
        # Информация о Sender ( пользователь который вызвал данную команду )
        self.sender = sender
        self.senderCanPerm = senderCanPerm
        # Диалог в котором была вызвана команда
        self.dialog = dialog
        # На кого направлена команда
        self.aimed = User
        self.canGetAimed = canGetAimed
        # Остальное
        self.errorType = errorMsgType
        self.obj = obj
        self.args = self.obj['text'].split()[1:]

    def getAimed(self):
        if 'reply_message' in self.obj.keys():
            return str(self.obj['reply_message']['from_id'])
        else:
            aimedId = ''
            for i in self.args[0]:
                if i == '|':
                    self.args = self.args[1:]
                    return aimedId
                elif not i.isalpha() and i != "[":
                    aimedId += i

    # Запускаем команду
    def initialize(self):
        if not self.senderCanPerm:
            self.dialog.msg(text=getError("userNotPerms").format(self.sender.ping()))
            return
        try:
            if self.canGetAimed:
                self.aimed = self.aimed(self.getAimed())
                if self.aimed.getRankID() < self.sender.getRankID():
                    try:
                        self.onCommand()
                    except:
                        self.dialog.msg(text=getError("commandRuneTimeError"))
                else:
                    self.dialog.msg(text=getError("commandNoUseInAimed").format(self.aimed.getRank().getName(),
                                                                                self.aimed.ping()))
                    return
            else:
                try:
                    self.onCommand()
                except:
                    self.dialog.msg(text=getError("commandRuneTimeError"))
        except:
            self.dialog.msg(text=self.errorType)
            return

    # сама команда
    def onCommand(self):
        pass
