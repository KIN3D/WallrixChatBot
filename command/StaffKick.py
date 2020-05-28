# Автор: Krashe85 vk:@Krashe85
from system.Command import BaseCommand
from system.answer import getInfraction
from lib.db import DB
from lib.tools import getAllDialogs


class StaffKickCommand(BaseCommand):
    def onCommand(self):
        secondDialogList = getAllDialogs()
        self.aimed.setRank(0)
        for i in secondDialogList:
            if i.getType() == 'staff':
                i.msg(text=getInfraction("staffKick").format(self.sender.getRank().getName(), self.sender.ping(),
                                                             self.aimed.ping()))
                i.kickUser(self.aimed)
        DB().createLogs(self.aimed, self.sender, "staff_kick", 0, "Более не является персоналом проекта")
