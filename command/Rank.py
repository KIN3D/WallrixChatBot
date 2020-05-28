# Автор: Krashe85 vk:@Krashe85
from system.Command import BaseCommand
from system.answer import getError, getInfo


class RankCommand(BaseCommand):
    def onCommand(self):
        # не забудь это настроить!
        getRank = int(self.args[0])
        maxRank = 10
        srModerRank = 1
        srModerMaxRank = 3
        if self.sender.getRankID() == srModerRank and getRank >= srModerMaxRank:
            self.dialog.msg(text=getError("manySetRank").format(self.sender.ping()))
            return
        if getRank > maxRank:
            self.dialog.msg(text=getError("maxRank").format(maxRank))
            return
        if int(self.aimed.getRankID()) > getRank:
            self.dialog.msg(text=getInfo("rankEdit").format(self.sender.getRank().getName(), self.sender.ping(),
                                                            "понизил", self.aimed.ping()))
            self.aimed.setRank(getRank)
        elif int(self.aimed.getRankID()) < getRank:
            self.dialog.msg(text=getInfo("rankEdit").format(self.sender.getRank().getName(), self.sender.ping(),
                                                            "повысил", self.aimed.ping()))
            self.aimed.setRank(getRank)
        elif int(self.aimed.getRank()) == getRank:
            self.dialog.msg(text=getError("rankAlreadyInstalled"))



