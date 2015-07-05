from celery import Celery


class BaseClient(object):

    def __init__(self, rabbit_url, module_name):
        self._app = Celery(module_name, broker=rabbit_url, backend=rabbit_url)

    def send_pin_task(self, task, pin_num):
        result = self._app.send_task(task, [pin_num])
        while not result.ready():
            pass
        return result.result
