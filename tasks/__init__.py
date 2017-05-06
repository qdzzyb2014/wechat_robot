from celery import Celery
import config


def create_celery():
    celery = Celery('wechat_robot', broker=config.CELERY_BROKER_URL)
    celery.config_from_object(config, force=True)
    return celery


celery_client = create_celery()

from . import wechat_tasks
