from celery import Celery


class GPIOClient(object):

    def __init__(self, rabbit_url):
        self._app = Celery('control', broker=rabbit_url, backend=rabbit_url)

    def _send_pin_task(self, task, pin_num):
        result = self._app.send_task(task, [pin_num])
        while not result.ready():
            pass
        return result.result

    def read(self, pin_num):
        return self._send_pin_task('control.celery.pin_read', pin_num)

    def on(self, pin_num):
        return self._send_pin_task('control.celery.pin_on', pin_num)

    def off(self, pin_num):
        return self._send_pin_task('control.celery.pin_off', pin_num)
