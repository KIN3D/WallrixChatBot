# Автор: Krashe85 vk:@Krashe85
from system.Command import BaseCommand
from system.answer import getInfraction, getError


class UnBanCommand(BaseCommand):
    def onCommand(self):
        if not self.dialog.inBanUser(self.aimed):
            self.dialog.msg(text=getError("userNotBan").format(self.aimed.ping()))
            return
        self.dialog.unBanUser(self.aimed)
        self.dialog.msg(text=getInfraction("userUnBan").format(self.sender.getRank().getName(), self.sender.ping(),
                                                               self.aimed.getRank().getName(), self.aimed.ping()))
