# Автор: Krashe85 vk:@Krashe85
from system.User import User
from system.Conversation import Dialog
from system.answer import getError, getInfraction, getInfo, getSpecial
from system.Rank import Rank
from jsons.reader import SettingsInType
# Импортируем команды
from command.Ban import BanCommand
from command.BlackList import BlackListCommand
from command.DialgModeEdit import EditModeCommand
from command.EditDialogStatus import EditDialogStatusCommand
from command.Help import HelpCommand
from command.History import HistoryCommand
from command.Kick import KickCommand
from command.Mute import MuteCommand
from command.Nick import NickCommand
from command.Notice import NoticeCommand
from command.Pardon import PardonCommand
from command.Rank import RankCommand
from command.StaffKick import StaffKickCommand
from command.UnBan import UnBanCommand
from command.UnMute import UnMuteCommand
from command.Who import WhoCommand


class Handler:
    def __init__(self, obj):
        self.obj = obj['object']
        self.dialog = Dialog(self.obj)

    # Первая проверка, на активацию диалого, бан пользователя и тд.
    def firstLevel(self):
        if not self.dialog.inActivate():
            self.dialog.msg(text=getError("dialogNotActivate"))
            return
        # Получем пользователя
        if 'action' in self.obj['message'].keys() and self.obj['message']['action']['type'] == 'chat_invite_user':
            inviteU = True
            userinvite = User(id=self.obj['message']['from_id'])
            user = User(id=self.obj['message']['action']['member_id'])
        else:
            inviteU = False
            userinvite = ''
            user = User(id=self.obj['message']['from_id'])
        userInviteInDialog = False
        if 'action' in self.obj['message'].keys():
            if self.obj['message']['action']['type'] == 'chat_invite_user' or self.obj['message']['action']['type'] == 'chat_invite_user_by_link':
                userInviteInDialog = True
                #self.dialog.msg(text=getSpecial("inviteUser").format(user.ping()))
                pass
            elif self.obj['message']['action']['type'] == 'chat_kick_user':
                if self.dialog == 'staff':
                    sType = 'leaveUserStaff'
                    self.dialog.kickUser(user)
                else:
                    sType = 'leaveUser'
                self.dialog.msg(text=getSpecial(sType).format(user.ping()))
                return
        # Проверяем пользовотеля на чс
        if user.inBlackList():
            self.dialog.msg(text=getInfraction("userInBlackList").format(user.ping()))
            self.dialog.kickUser(user)
            if self.dialog.inSilenceMode():
                self.dialog.msg(text=getInfo("silenceModeInDialogAlarm").format(self.dialog.getTextSilenceMode()))
            return
        # Проверка на МУТ
        if self.dialog.inMuteUser(user):
            if inviteU:
                if Rank(userinvite).canRazMute():
                    self.dialog.msg(text=getInfraction("userUnMuteByInvite").format(user.ping(),
                                                                                    userinvite.getRank().getName(),
                                                                                    userinvite.ping()))
                    self.dialog.unMuteUser(user)
                    return
            self.dialog.msg(text=getInfraction("userViolatedMute").format(user.ping()))
            self.dialog.kickUser(user)
            if self.dialog.inSilenceMode():
                self.dialog.msg(text=getInfo("silenceModeInDialogAlarm").format(self.dialog.getTextSilenceMode()))
            return
        # Проверка на БАН
        if self.dialog.inBanUser(user):
            if inviteU:
                if Rank(userinvite).canRazBan():
                    self.dialog.msg(text=getInfraction("userUnBanByInvite").format(user.ping(),
                                                                                   userinvite.getRank().getName(),
                                                                                   userinvite.ping()))
                    self.dialog.unBanUser(user)
            self.dialog.msg(text=getInfraction("userViolatedBan").format(user.ping()))
            self.dialog.kickUser(user)
            if self.dialog.inSilenceMode():
                self.dialog.msg(text=getInfo("silenceModeInDialogAlarm").format(self.dialog.getTextSilenceMode()))
            return
        # Проверка на режим молчания
        if self.dialog.inSilenceMode():
            if not user.getRank().canIgnoreSilenceMode() and not userInviteInDialog:
                self.dialog.muteUser(user, 600)
                self.dialog.msg(
                    text=getInfraction("userViolatedSilenceMode").format(user.getRank().getName(), user.ping()))
                self.dialog.msg(text=getInfo("mute").format(user.ping(), "5 минут"))
                self.dialog.msg(text=getInfo("silenceModeInDialogAlarm").format(self.dialog.getTextSilenceMode()))
                return
        if userInviteInDialog:
            self.dialog.msg(text=getSpecial("inviteUser").format(user.ping()))
        if self.dialog.getType() == 'staff':
            return self.secondLevel(user)
        # Проверка на запрещённые слова
        text = self.obj['message']['text'].split()
        for i in text:
            if i.lower() in SettingsInType('mat'):
                if not user.getRank().canIgnoreMat():
                    self.dialog.muteUser(user, 900)
                    self.dialog.msg(
                        text=getInfraction("userMute").format("Святой", "Ботя", user.getRank().getName(), user.ping(),
                                                              "15м", "Использование запрещённых слов"))
                    self.dialog.msg(text=getInfo("mute").format(user.ping(), "15м"))
                    return
        return self.secondLevel(user)
        
    # Вызываем команду
    def secondLevel(self, user):
        commandList = {
            "бан": BanCommand(sender=user, dialog=self.dialog, errorMsgType=getError("banError"),
                              senderCanPerm=user.getRank().canBan(), obj=self.obj['message']),

            "чс": BlackListCommand(sender=user, dialog=self.dialog, errorMsgType=getError("blackListError"),
                                   senderCanPerm=user.getRank().canBlackList(), obj=self.obj['message']),

            "режим": EditModeCommand(sender=user, dialog=self.dialog, errorMsgType=getError("modeError"),
                                     senderCanPerm=user.getRank().canEditDialogMode(), obj=self.obj['message'],
                                     canGetAimed=False),

            "помощь": HelpCommand(sender=user, dialog=self.dialog, errorMsgType=getError("helpError"),
                                  senderCanPerm=user.getRank().canHelp(), obj=self.obj['message'], canGetAimed=False),

            "история": HistoryCommand(sender=user, dialog=self.dialog, errorMsgType=getError("historyError"),
                                      senderCanPerm=user.getRank().canHistory(), obj=self.obj['message']),

            "кик": KickCommand(sender=user, dialog=self.dialog, errorMsgType=getError("kickError"),
                               senderCanPerm=user.getRank().canNick(), obj=self.obj['message']),

            "мут": MuteCommand(sender=user, dialog=self.dialog, errorMsgType=getError("muteError"),
                               senderCanPerm=user.getRank().canMute(), obj=self.obj['message']),

            "ник": NickCommand(sender=user, dialog=self.dialog, errorMsgType=getError("nickError"),
                               senderCanPerm=user.getRank().canNick(), obj=self.obj['message'], canGetAimed=False),

            "объявление": NoticeCommand(sender=user, dialog=self.dialog, errorMsgType=getError("noticeError"),
                                        senderCanPerm=user.getRank().canNotice(), obj=self.obj['message'],
                                        canGetAimed=False),

            "помиловать": PardonCommand(sender=user, dialog=self.dialog, errorMsgType=getError("pardonError"),
                                        senderCanPerm=user.getRank().canPardon(), obj=self.obj['message']),

            "ранг": RankCommand(sender=user, dialog=self.dialog, errorMsgType=getError("rankError"),
                                senderCanPerm=user.getRank().canRank(), obj=self.obj['message']),

            "стафф-кик": StaffKickCommand(sender=user, dialog=self.dialog, errorMsgType=getError("staffKickError"),
                                          senderCanPerm=user.getRank().canStaffKick(), obj=self.obj['message']),

            "разбан": UnBanCommand(sender=user, dialog=self.dialog, errorMsgType=getError("unBanError"),
                                   senderCanPerm=user.getRank().canRazBan(), obj=self.obj['message']),

            "размут": UnMuteCommand(sender=user, dialog=self.dialog, errorMsgType=getError("unMuteError"),
                                    senderCanPerm=user.getRank().canRazMute(), obj=self.obj['message']),

            "!кто": WhoCommand(sender=user, dialog=self.dialog, errorMsgType=getError("whoError"),
                               senderCanPerm=user.getRank().canWho(), obj=self.obj['message']),

            "!статус": EditDialogStatusCommand(sender=user, dialog=self.dialog, errorMsgType=getError("activateError"),
                                               senderCanPerm=user.getRank().canEditDialogStatus(),
                                               obj=self.obj['message'], canGetAimed=False),
        }
        try:
            commandList[self.obj['message']['text'].split()[0].lower()].initialize()
        except:
            pass
