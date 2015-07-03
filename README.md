# Pi-Celery-GPIO
Examples combining Celery (http://www.celeryproject.org/) and [Raspberry Pi GPIO](https://www.raspberrypi.org/documentation/usage/gpio/)



## Raspberry Pi

* This directory (`/raspberry_pi`) contains examples of Celery workers meant to run on a Raspberry Pi.
* The `/raspberry_pi/requirements.txt` file tracks all the Python dependencies for the examples in this directory. To manually install: `sudo pip install -r requirements.txt`.
* The `/raspberry_pi/control` directory contains a Celery worker that receives tasks to control the Raspberry Pi's GPIO pins.


### Controlling GPIO

Export the following environment variables before starting the worker:
* `CONTROL_RABBIT_URL`: The [RabbitMQ](https://www.rabbitmq.com/) connection URL for the [Celery broker](http://celery.readthedocs.org/en/latest/getting-started/brokers/rabbitmq.html).
* `CONTROL_PIN_CONFIG`: The path to a [config file](https://github.com/projectweekend/Pi-Pin-Manager#configure-it) that defines the pins available to be controlled. **Note:** This worker only receives messages to flip or read GPIO pins so the config `mode` should always be set to `OUT`.
* `C_FORCE_ROOT`: Set this to `True` because the Raspberry Pi GPIO access requires root access.

Start the `control` Celery worker by running this command inside the `/raspberry_pi` directory:
```
sudo -E celery -A control worker
```

### Using the GPIO Client

In the `/client` package there is a class to use for interacting with the Raspberry Pi that is running the `control` Celery worker. You can run this from anywhere that can connect to the same RabbitMQ instance referenced in `CONTROL_RABBIT_URL`.

**Example:**
```python
from client.gpio import GPIOClient

# Set this to the same connection URL used in CONTROL_RABBIT_URL
CONTROL_RABBIT_URL = ''

# Create an instance of the class
client = GPIOClient(CONTROL_RABBIT_URL)

# Turn pin on (result will be 1)
result = client.on(18)

# Turn pin off (result will be 0)
result = client.off(18)

# Read pin state (result will be 0 or 1)
result = client.read(18)
```
