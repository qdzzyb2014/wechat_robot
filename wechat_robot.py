import requests
import itchat

import config

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
    weather_msg = get_response('{}天气'.format(user.get('City')))
    wechat_assistant.send_msg(weather_msg, user.get('UserName'))


def fetch_users():
    return wechat_assistant.get_friends()[:1]


if __name__ == '__main__':
    wechat_assistant.auto_login(hotReload=True)
    wechat_assistant.run()
