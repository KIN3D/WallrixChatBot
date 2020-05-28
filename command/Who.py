# Автор: Krashe85 vk:@Krashe85
from system.Command import BaseCommand
from system.answer import getInfo, getError


class WhoCommand(BaseCommand):
    def onCommand(self):
        self.dialog.msg(text=getInfo("whoInfoCommand").format(
            self.aimed.pingName(), self.aimed.getFirstName(), self.aimed.getLastName(), self.aimed.getNick(),
            self.aimed.getRank().getName(), self.dialog.inMuteUser(self.aimed),
            self.dialog.inBanUser(self.aimed), self.aimed.inBlackList(), len(self.aimed.getHistory())))

    def initialize(self):
        try:
            self.aimed = self.aimed(id=self.getAimed())
            self.onCommand()
        except:
            self.dialog.msg(text=getError("whoError"))
