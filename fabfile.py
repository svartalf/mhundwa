# -*- coding: utf-8 -*-

import os

from fabric.api import env, sudo

import settings


HOSTS = getattr(settings, 'DEPLOY_HOSTS', ())

PROJECT_ROOT = getattr(settings, 'DEPLOY_ROOT', '/var/www/mhundwa')
ENV_FOLDER = getattr(settings, 'DEPLOY_ENV_FOLDER', '.env')

# Список доменов для подключения
env.hosts = HOSTS


def deploy():
    sudo('cd {}; git pull'.format(PROJECT_ROOT))

    sudo('{} install -r {}'.format(
        os.path.join(PROJECT_ROOT, ENV_FOLDER, 'bin/pip'),
        os.path.join(PROJECT_ROOT, 'requirements.txt'),
    ))
