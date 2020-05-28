from flask import Flask
from lib.db import DB
from flask import make_response
from handler import Handler
from jsons.reader import SettingsInType
from system.User import User
from system.Conversation import Dialog
from system.answer import getInfraction
from flask import json
from flask import request
import time

app = Flask(__name__)


@app.route('/callback', methods=['POST', 'GET'])
def vk():
    # Распаковываем jsons из пришедшего POST-запроса
    try:
        data = json.loads(request.get_data())
        # Проверяем от вк ли запросe
        # Если подтверждение URL
        if data['type'] == 'confirmation':
            resp_text = SettingsInType('confirmation_code')
            # Если новое сообщение
        elif data['type'] == 'message_new':
            Handler(data).firstLevel()
            resp_text = 'OK'
        return make_response(resp_text, 200)
    except:
        return make_response("OK", 200)


        
if __name__ == '__main__':
    app.run()

