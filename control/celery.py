from __future__ import absolute_import
import os
from celery import Celery
from pi_pin_manager import PinManager


RABBIT_URL = os.getenv('CONTROL_RABBIT_URL')
assert RABBIT_URL

CONTROL_PIN_CONFIG = os.getenv('CONTROL_PIN_CONFIG')
assert CONTROL_PIN_CONFIG


pins = PinManager(config_file=CONTROL_PIN_CONFIG)


app = Celery('control', broker=RABBIT_URL, backend=RABBIT_URL)
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=86400,
    BROKER_CONNECTION_TIMEOUT=10
)


@app.task
def pin_on(pin_num):
    pins.on(pin_num)


@app.task
def pin_off(pin_num):
    pins.off(pin_num)


@app.task
def pin_read(pin_num):
    return pins.read(pin_num)


if __name__ == '__main__':
    app.start()
