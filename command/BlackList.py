# Автор: Krashe85 vk:@Krashe85
from system.Command import BaseCommand
from system.answer import getInfraction
from lib.tools import getAllDialogs
from lib.db import DB


class BlackListCommand(BaseCommand):
    def onCommand(self):
        dialogsList = getAllDialogs()
        self.aimed.setBalckList()
        self.dialog.msg(
            text=getInfraction("userAddBlackList").format(self.sender.getRank().getName(), self.sender.ping(),
                                                          self.aimed.getRank().getName(), self.aimed.ping()))
        self.dialog.kickUser(self.aimed)
        for i in dialogsList:
            i.kickUser(self.aimed)
        DB().createLogs(self.aimed, self.sender, "back_list", 0, "NONE")
