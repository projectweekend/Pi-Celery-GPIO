from client.client import BaseClient


class GPIOClient(BaseClient):

    def __init__(self, rabbit_url):
        super(GPIOClient, self).__init__(rabbit_url, 'control')

    def read(self, pin_num):
        return self.send_pin_task('control.celery.pin_read', pin_num)

    def on(self, pin_num):
        return self.send_pin_task('control.celery.pin_on', pin_num)

    def off(self, pin_num):
        return self.send_pin_task('control.celery.pin_off', pin_num)
