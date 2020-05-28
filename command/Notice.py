# Автор: Krashe85 vk:@Krashe85
from system.Command import BaseCommand
from system.answer import getInfo, getError
from lib.tools import getAllDialogs, getReason


class NoticeCommand(BaseCommand):
    def onCommand(self):
        if len(self.args) == 0:
            self.dialog.msg(text=getError("noticeError"))
            return
        dialgoType = self.args[0].lower()
        dt = 'NONE'
        dialogList = getAllDialogs()
        if dialgoType == 'персонал' or dialgoType == 'staff':
            dt = 'staff'
        elif dialgoType == 'игроки' or dialgoType == 'users':
            dt = 'user'
        elif dialgoType == 'специальный' or dialgoType == 'special':
            dt = 'special'
        elif dialgoType == 'все' or dialgoType == 'all':
            dt = 'all'
        for i in dialogList:
            if dt == 'all' or i.getType() == dt:
                i.msg(text="Объявление от {}\n{}\n@all".format(self.sender.ping(), getReason(self.args[1:])))
        self.dialog.msg(text=getInfo("noticeSuccess").format(self.sender.getRank().getName(), self.sender.ping(),
                                                             dt))


