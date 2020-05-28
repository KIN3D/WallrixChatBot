# Автор: Krashe85 vk:@Krashe85
import json


def main(file):
    with open(file, "r") as read_file:
        data = json.load(read_file)
    return data


def SettingsInType(type):
    return main("settings.json").get(type)


def getRankNameInId(rid):
    return main("rankName.json").get(str(rid.user.getRankID()))


def AnswerFile():
    return main("answer.json")
