# Pi-Celery-GPIO
Examples combining Celery (http://www.celeryproject.org/) and [Raspberry Pi GPIO](https://www.raspberrypi.org/documentation/usage/gpio/)



## Service

* This directory (`/service`) contains examples of Celery workers meant to run on a Raspberry Pi.
* The `/service/requirements.txt` file tracks all the Python dependencies for the examples in this directory. To manually install: `sudo pip install -r requirements.txt`.
* The `/service/control` directory contains a Celery worker that receives tasks to control the Raspberry Pi's GPIO pins.


### Using /service/control

Export the following environment variables before starting the worker:
* `CONTROL_RABBIT_URL`: The [RabbitMQ](https://www.rabbitmq.com/) connection URL for the [Celery broker](http://celery.readthedocs.org/en/latest/getting-started/brokers/rabbitmq.html).
* `CONTROL_PIN_CONFIG`: The path to a [config file](https://github.com/projectweekend/Pi-Pin-Manager#configure-it) that defines the pins available to be controlled.
* `C_FORCE_ROOT`: Set this to `True` because the Raspberry Pi GPIO access requires root access.

Start the Celery worker by running this command inside the `/service/control` directory:
```
sudo -E celery -A control worker
```
