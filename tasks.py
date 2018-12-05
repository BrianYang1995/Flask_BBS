from celery import Celery
from flask import Flask
from flask_mail import Message

import config
import json
from exts import mail
from exts import alidayu

app = Flask(__name__)
app.config.from_object(config)
mail.init_app(app)
alidayu.init_app(app)


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)


@celery.task()
def send_email(object, email, context):
    message = Message(object, recipients=email, html=context)
    mail.send(message)


@celery.task()
def send_sms(telephone, captcha):
    alidayu.send_sms(telephone, key=captcha)


