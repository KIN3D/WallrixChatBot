from system.Command import BaseCommand
from system.answer import getInfo, getError
from lib.tools import getReason


class EditModeCommand(BaseCommand):
    def onCommand(self):
        if len(self.args) == 0:
            self.dialog.msg(text=getError("modeError"))
        newMode = self.args[0].lower()
        if newMode == 'молчание':
            self.dialog.activateSilenceMode(text=getReason(self.args[1:]))
            self.dialog.msg(text=getInfo("editGroupMode").format(self.sender.getRank().getName(), self.sender.ping(),
                                                                 newMode))
            self.dialog.msg(text=getInfo("activateSilenceMode"))
        elif newMode == 'разговор':
            self.dialog.activateSpeakMode()
            self.dialog.msg(text=getInfo("editGroupMode").format(self.sender.getRank().getName(), self.sender.ping(),
                                                                 newMode))
        else:
            self.dialog.msg(text=getError("unknownParam"))