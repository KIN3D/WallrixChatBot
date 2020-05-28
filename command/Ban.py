# Автор: Krashe85 vk:@Krashe85
from system.Command import BaseCommand
from system.answer import getInfraction, getError
from lib.tools import violationLimits, getInfractionTime, getReason
from lib.db import DB


class BanCommand(BaseCommand):
    def onCommand(self):
        time = getInfractionTime(self.args[0])
        if not time:
            self.dialog.msg(text=getError("timeError").format(self.sender.ping()))
            return 
        if self.dialog.inBanUser(self.aimed):
            self.dialog.msg(text=getError("userAlreadyBan").format(self.aimed.ping()))
            return
        if violationLimits(self.sender, time):
            self.dialog.msg(text=getError("rankLimit").format(self.sender.getRank().getName(), self.sender.ping(),
                                                              self.sender.getRank().getInfractionLimit()))
            return
        self.dialog.banUser(self.aimed, time)
        DB().createLogs(self.aimed, self.sender, "ban", time, getReason(self.args[1:]))
        self.dialog.msg(text=getInfraction("userBan").format(self.sender.getRank().getName(), self.sender.ping(),
                                                             self.aimed.getRank().getName(), self.aimed.ping(),
                                                             self.args[0], getReason(self.args[1:])))
        self.dialog.kickUser(self.aimed)
