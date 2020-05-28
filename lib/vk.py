# Автор: Krashe85 vk:@Krashe85
import random

import requests

from jsons.reader import SettingsInType


class Vk:
    def __init__(self):
        self.server = SettingsInType('api_server')
        self.token = SettingsInType('token')
        self.api_version = SettingsInType('api_version')

    # Отправка запроса на сервер
    def call(self, method, param):
        param['access_token'] = self.token
        param['v'] = self.api_version
        r = requests.get("{}{}".format(self.server, method), params=param).json()
        # Проверяем не вернулась ли ошибка
        if 'error' in r.keys():
            print('[VK ERROR] when executing the method {}'.format(method))
            print('[VK ERROR] code: {}'.format(r['error']['error_code']))
            print('[VK ERROR] message: {}'.format(r['error']['error_msg']))
            return
        # Возврашаем ответ сервера
        else:
            return r

    def message(self, peer, text):
        return self.call(method="messages.send", param={"random_id": random.randint(1, 2 ** 120),
                                                        "peer_id": peer, "message": text})

    def user_info(self, id):
        return self.call(method="users.get", param={"user_ids": id})['response'][0]

    def kick(self, peer_id, user_id):
        return self.call(method="messages.removeChatUser", param={"chat_id": peer_id - 2000000000, "user_id": user_id})
