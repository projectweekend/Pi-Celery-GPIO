# Pi-Celery-GPIO
Examples combining Celery (http://www.celeryproject.org/) and Raspberry Pi GPIO

## Control

The `/control` directory contains a Celery worker that processes tasks to control the Raspberry Pi's GPIO pins.

Export the following environment variables before starting the worker:
* `CONTROL_RABBIT_URL`: The [RabbitMQ](https://www.rabbitmq.com/) connection URL for the [Celery broker](http://celery.readthedocs.org/en/latest/getting-started/brokers/rabbitmq.html).
* `CONTROL_PIN_CONFIG`: The path to a [config file](https://github.com/projectweekend/Pi-Pin-Manager#configure-it) that defines the pins available to be controlled.
* `C_FORCE_ROOT`: Set this to `True` because the Raspberry Pi GPIO access requires root access.

Start the Celery worker by running this command inside the `/control` directory:
```
sudo -E celery -A control worker
```
