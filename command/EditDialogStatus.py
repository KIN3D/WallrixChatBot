from system.Command import BaseCommand
from system.answer import getError, getInfo


class EditDialogStatusCommand(BaseCommand):
    def onCommand(self):
        if len(self.args) == 0:
            self.dialog.msg(text=getError("activateError"))
            return
        newStatus = self.args[0].lower()
        newType = self.args[1].lower()
        if newStatus == 'активировать':
            self.dialog.activate()
            self.dialog.editType(newType)
            if newType == 'staff' or newType == 'user' or newType == 'special':
                self.dialog.msg(text=getInfo("activateDialog").format(self.sender.getRank().getName(),
                                                                      self.sender.ping(), newType))
            else:
                self.dialog.msg(text=getError("unknownParam"))
        elif newType == 'деактивировать':
            self.dialog.deactivate()
        else:
            self.dialog.msg(text=getError("unknownParam"))