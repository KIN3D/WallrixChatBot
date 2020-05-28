# Автор: Krashe85 vk:@Krashe85
from system.Command import BaseCommand
from system.answer import getInfo


class HelpCommand(BaseCommand):
    def onCommand(self):
        commandList = self.sender.getRank().commandsInRank()
        helpList = ''
        for i in commandList:
            helpList += 'команда {}\n'.format(i)
        self.dialog.msg(text=getInfo("userHelp").format(self.sender.getRank().getName(),
                                                        self.sender.ping(), helpList))
