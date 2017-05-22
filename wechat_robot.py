import logging
from threading import Thread
from datetime import datetime
from time import sleep
import requests
import itchat

from itchat.components.register import logger
from itchat.log import set_logging

import config

KEY = 'ad65aa94781643e682cd81a629fdecc4'

wechat_assistant = itchat.new_instance()

tasks = []


def append_task(func):
    tasks.append(Thread(target=func))
    return func


def run(self, debug=False, block_thread=True):
    logger.info('Start auto replying.')
    setattr(self, 'debug', debug)
    for task in tasks:
        task.start()
    if debug:
        set_logging(loggingLevel=logging.DEBUG)
    else:
        set_logging(loggingFile='wechat_robot.log')

    def reply_fn():
        try:
            while self.alive:
                self.configured_reply()
        except KeyboardInterrupt:
            if self.useHotReload:
                self.dump_login_status()
            self.alive = False
            for task in tasks:
                task.join()
            logger.debug('itchat received an ^C and exit.')
            logger.info('Bye~')
    if block_thread:
        reply_fn()
    else:
        replay_thread = Thread(target=reply_fn)
        replay_thread.setDaemon(True)
        replay_thread.start()


wechat_assistant.run = run


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
        return 'request tuling error'


@wechat_assistant.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    default_reply = 'I received: ' + msg['Text']
    reply = get_response(msg['Text'])
    return reply or default_reply


def send_weather(user):
    city = user.get('City')
    if not city:
        return
    weather_msg = get_response('{}天气'.format(city))
    wechat_assistant.send_msg(weather_msg, user.get('UserName'))


def fetch_users():
    if wechat_assistant.debug:
        return wechat_assistant.search_friends(nickName='低位自嗨')
    return wechat_assistant.get_friends()


@append_task
def send_test_msg():
    msg = 'test'
    user = fetch_users()[0]
    while wechat_assistant.alive and wechat_assistant.debug:
        wechat_assistant.send_msg(msg, user.get('UserName'))
        sleep(5)


@append_task
def send_weather_to_all_friends():
    while wechat_assistant.alive:
        current_time = datetime.now()
        if (current_time.minute == 20 and
                current_time.hour == 7 and
                current_time.second == 0):
            for u in fetch_users():
                send_weather(u)
        sleep(1)


@append_task
def remind_report():
    while wechat_assistant.alive:
        current_time = datetime.now()
        user = wechat_assistant.search_friends(nickName='低位自嗨')[0]
        if (current_time.hour == 16 and current_time.minute == 45 and current_time.second == 0):
            wechat_assistant.send_msg('get ready for scrum', user)
        elif (current_time.hour == 17 and current_time.minute == 0 and current_time.second == 0):
            wechat_assistant.send_msg('scrum!', user)
        sleep(1)


if __name__ == '__main__':
    wechat_assistant.auto_login(hotReload=True, enableCmdQR=2)
    run(wechat_assistant, debug=config.DEBUG)
