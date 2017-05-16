from celery.schedules import crontab


DEBUG = True

CELERY_BROKER_URL = 'redis://localhost:6379/0'
ONCE_REDIS_URL = 'redis://localhost:6379/0'

CELERY_TASK_SERIALIZER = 'json'
CELERYD_TASK_SOFT_TIME_LIMIT = 300
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

CELERYBEAT_SCHEDULE = {
    'push_weather': {
        'push_weather': crontab(minute=30, hour=8)
    }
}
