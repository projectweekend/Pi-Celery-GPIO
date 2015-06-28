import os
from pi_pin_manager import PinManager
from control.celery import app


CONTROL_PIN_CONFIG = os.getenv('CONTROL_PIN_CONFIG')
assert CONTROL_PIN_CONFIG


pins = PinManager(config_file=CONTROL_PIN_CONFIG)


@app.task
def pin_on(pin_num):
    pins.on(pin_num)


@app.task
def pin_off(pin_num):
    pins.off(pin_num)
