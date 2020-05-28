# Автор: Krashe85 vk:@Krashe85
from system.Command import BaseCommand
from system.answer import getInfraction, getError, getInfo
from lib.tools import violationLimits, getInfractionTime, getReason
from lib.db import DB


class MuteCommand(BaseCommand):
    def onCommand(self):
        time = getInfractionTime(self.args[0])
        if not time:
            self.dialog.msg(text=getError("timeError").format(self.sender.ping()))
            return 
        if self.dialog.inMuteUser(self.aimed):
            self.dialog.msg(text=getError("userAlreadyMute").format(self.aimed.ping()))
            return
        if violationLimits(self.sender, time):
            self.dialog.msg(text=getError("rankLimit").format(self.sender.getRank().getName(), self.sender.ping(),
                                                              self.sender.getRank().getInfractionLimit()))
            return
        self.dialog.muteUser(self.aimed, time)
        DB().createLogs(self.aimed, self.sender, "mute", time, getReason(self.args[1:]))
        self.dialog.msg(text=getInfraction("userMute").format(self.sender.getRank().getName(), self.sender.ping(),
                                                              self.aimed.getRank().getName(), self.aimed.ping(),
                                                              self.args[0], getReason(self.args[1:])))
        self.dialog.msg(text=getInfo("mute").format(self.aimed.ping(), getReason(self.args[0])))

