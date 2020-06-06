# Автор: Krashe85 vk:@Krashe85
from system.Command import BaseCommand
from system.answer import getInfo, getError


class NickCommand(BaseCommand):
    def onCommand(self):
        if len(self.args) == 0:
            self.dialog.msg(text=getError("nickError"))
        if self.args[0].lower() == 'уст':
            newNick = self.args[1]
            self.sender.setNick(newNick)
            self.sender.refreshInfo()
            self.dialog.msg(text=getInfo("successfulNicknameChange").format(self.sender.getFirstName(),
                                                                            self.sender.getNick()))
        elif self.args[0].lower() == 'сбросить':
            newNick = self.sender.getFirstName()
            self.sender.setNick(newNick)
            self.dialog.msg(text=getInfo("successfulNicknameReset").format(self.sender.getFirstName()))
        else:
            self.dialog.msg(text=getError("unknownParam"))

