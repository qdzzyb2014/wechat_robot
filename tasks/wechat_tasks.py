from celery.utils.log import get_task_logger

from wechat_robot import wechat_assistant
from wechat_robot import send_weather
from . import celery_client


logger = get_task_logger('Wechat Tasks')


@celery_client.task(name='push_weather')
def weather():
    wechat_assistant.auto_login(hotReload=True)
    users = wechat_assistant.get_friends()
    for user in users:
        try:
            send_weather(user)
        except Exception as e:
            logger.error(e)
