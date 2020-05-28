# Автор: Krashe85 vk:@Krashe85
from system.Command import BaseCommand
from system.answer import getInfraction, getError


class UnMuteCommand(BaseCommand):
    def onCommand(self):
        if not self.dialog.inMuteUser(self.aimed):
            self.dialog.msg(text=getError("userNotMute").format(self.aimed.ping()))
            return
        self.dialog.unMuteUser(self.aimed)
        self.dialog.msg(text=getInfraction("userUnMute").format(self.sender.getRank().getName(), self.sender.ping(),
                                                                self.aimed.getRank().getName(), self.aimed.ping()))
