from StringIO import StringIO
from fabric import api
from fabric.contrib.files import exists


def celery_control_prompts():
    data = {}
    data['host_ip'] = api.prompt('Host IP:')
    data['host_user'] = api.prompt('Host user:')
    data['rabbit_url'] = api.prompt('RabbitMQ URL:')
    data['pin_config'] = api.prompt('Pin config file:')
    data['install_path'] = api.prompt('Install path:')
    return data


def celery_control_upstart_script(data):
    template = """
    description "Pi-Celery-GPIO Control"
    start on runlevel [2345]
    stop on runlevel [06]
    respawn
    respawn limit 10 5

    env CONTROL_RABBIT_URL={rabbit_url}
    env CONTROL_PIN_CONFIG={pin_config}
    env C_FORCE_ROOT=True

    script
            cd {install_path}/Pi-Celery-GPIO/service && sudo -E celery -A control worker
    end script
    """

    upstart_script = StringIO(template.format(**data))
    with api.cd('/etc/init'):
        upload = api.put(upstart_script, 'gpio-control.conf', use_sudo=True)
        assert upload.succeeded


@api.task
def install_celery_control():
    data = celery_control_prompts()

    api.env.host_string = data['host_ip']
    api.env.user = data['host_user']

    api.sudo('apt-get update')
    api.sudo('echo Yes, do as I say! | apt-get -y --force-yes install upstart')

    with api.cd(data['install_path']):
        project_path = '{0}/Pi-Celery-GPIO'.format(data['install_path'])
        if exists(project_path, use_sudo=True):
            api.sudo('rm -r {0}'.format(project_path))

        api.sudo('git clone https://github.com/projectweekend/Pi-Celery-GPIO.git')
        with api.cd('Pi-Celery-GPIO/service'):
            api.sudo('pip install -r requirements.txt')

    celery_control_upstart_script(data)

    reboot = api.prompt('Install complete. Ready to reboot? (Y/N):')
    if reboot == 'Y':
        api.sudo('reboot')


@api.task
def update_celery_control():
    data = celery_control_prompts()

    api.env.host_string = data['host_ip']
    api.env.user = data['host_user']

    with api.settings(warn_only=True):
        api.sudo('service gpio-control stop')

    with api.cd(data['install_path']):
        project_path = '{0}/Pi-Celery-GPIO'.format(data['install_path'])
        if exists(project_path, use_sudo=True):
            api.sudo('rm -r {0}'.format(project_path))

        api.sudo('git clone https://github.com/projectweekend/Pi-Celery-GPIO.git')
        with api.cd('Pi-Celery-GPIO/service'):
            api.sudo('pip install -r requirements.txt')

    celery_control_upstart_script(data)

    api.sudo('service gpio-control start')
