
from __future__ import absolute_import
from celery import Celery

app = Celery('test_celery',
             broker='amqp://rabbit:rabbit@10.0.75.1//',
             backend='redis://10.0.75.1:6379/0',
             include=['test_celery.tasks'])