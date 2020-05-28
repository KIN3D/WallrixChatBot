# Автор: Krashe85 vk:@Krashe85
from system.Command import BaseCommand
from system.answer import getInfraction
from lib.tools import getAllDialogs


class PardonCommand(BaseCommand):
    def onCommand(self):
        if self.aimed.inBlackList():
            self.aimed.delBalckList()
        for i in getAllDialogs():
            if i.inBanUser(self.aimed):
                i.unBanUser(self.aimed)
            if i.inMuteUser(self.aimed):
                i.unMuteUser(self.aimed)
        self.dialog.msg(text=getInfraction("pardonUser").format(self.sender.getRank().getName(),
                                                                self.sender.ping(), self.aimed.ping()))
