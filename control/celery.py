from __future__ import absolute_import
import os
from celery import Celery


RABBIT_URL = os.getenv('CONTROL_RABBIT_URL')
assert RABBIT_URL


app = Celery('control', broker=RABBIT_URL, backend=RABBIT_URL, include=['control.tasks'])
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    BROKER_CONNECTION_TIMEOUT=10
)


if __name__ == '__main__':
    app.start()
