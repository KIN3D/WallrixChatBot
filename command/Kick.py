# Автор: Krashe85 vk:@Krashe85
from system.Command import BaseCommand
from system.answer import getInfraction
from lib.db import DB
from lib.tools import getReason


class KickCommand(BaseCommand):
    def onCommand(self):
        self.dialog.msg(text=getInfraction("userKick").format(self.sender.getRank().getName(), self.sender.ping(),
                                                              self.aimed.getRank().getName(), self.aimed.ping(),
                                                              getReason(self.args)))
        DB().createLogs(self.aimed, self.sender, "kick", 0, getReason(self.args))
        self.dialog.kickUser(self.aimed)
