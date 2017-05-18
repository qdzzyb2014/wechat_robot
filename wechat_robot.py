from threading import Thread
from datetime import datetime
from time import sleep
import requests
import itchat


KEY = 'ad65aa94781643e682cd81a629fdecc4'

wechat_assistant = itchat.new_instance()


def get_response(msg):
    api_url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(api_url, data=data).json()
        return r.get('text')
    except:
        return


@wechat_assistant.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    default_reply = 'I received: ' + msg['Text']
    reply = get_response(msg['Text'])
    return reply or default_reply


def send_weather(user):
    city = user.get('City')
    if not city:
        return
    weather_msg = get_response('{}天气'.format(user.get('City')))
    wechat_assistant.send_msg(weather_msg, user.get('UserName'))


def fetch_users():
    return wechat_assistant.get_friends()


def task_send_weather_to_all_friends():
    while True:
        current_time = datetime.now()
        if (current_time.minute == 20 and
                current_time.hour == 7 and
                current_time.second == 0):
            for u in fetch_users():
                send_weather(u)
        sleep(1)


if __name__ == '__main__':
    wechat_assistant.auto_login(hotReload=True, enableCmdQR=2)
    weather_thread = Thread(target=task_send_weather_to_all_friends)
    wechat_assistant.run(blockThread=False)
    weather_thread.start()
    while wechat_assistant.alive:
        pass
