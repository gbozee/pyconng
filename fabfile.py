import os
from fabric.api import local, run, cd, env, sudo, settings, lcd
from fabric.decorators import hosts
env.hosts = ['pycon@104.236.214.189']

password = os.getenv('PYCON_PRODUCTION_PASSWORD', '')


def common_code(code_dir):
    with settings(user="pycon", password=password):
        with cd(code_dir):
            run("pwd")
            run("git pull")
            sudo("docker-compose build")
            sudo("docker-compose kill django")
            sudo("docker-compose rm django")
            sudo("docker-compose up -d")
            sudo("docker-compose run django python manage.py collectstatic --noinput")
            sudo("docker-compose run django python manage.py migrate --noinput")


def deploy_current():
    print("hello World")
    run("pwd")
    code_dir = '/home/pycon/pyconng'
    common_code(code_dir)

def display_logs():
    with settings(user="pycon", password=password):
        cd("/home/pycon/pyconng")
        sudo("docker-compose logs --follow django")

def start():
    local('docker-compose -f dev.yml kill django')
    local('docker-compose -f dev.yml up -d django')

def logs():
    local('docker-compose -f dev.yml logs --follow --tail=10 django')
    
def console():
    local('docker exec -i -t pyconng_django_1 bash')