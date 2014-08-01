# coding=utf-8

from fabric.api import env, cd, run

USERNAME = 'fuse'
SERVER = 'octoberry.ru'
PROJECT_DIR = '/var/www/peerpay/repo'
VENV_DIR = '/var/www/peerpay/.env'

env.hosts = ["%s@%s" % (USERNAME, SERVER)]


def deploy():
    with cd(PROJECT_DIR):
        run('sudo git pull')
        run('sudo pyclean .')

        run('sudo %s/bin/pip install -q -r requirements.txt' % VENV_DIR)
        run('sudo %s/bin/yoyo-migrate -b apply migrations/' % VENV_DIR)

    run('sudo service uwsgi restart')