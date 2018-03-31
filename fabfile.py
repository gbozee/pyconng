import os
from fabric.api import local, run, cd, env, sudo, settings, lcd
from fabric.decorators import hosts
username = os.getenv('PYCON_USERNAME')
env.hosts = [f'{username}@www.pycon.ng']

password = os.getenv('PYCON_PRODUCTION_PASSWORD', '')


def common_code(code_dir):
    with settings(user=username, password=password):
        with cd(code_dir):
            run("pwd")
            run("git pull")
            sudo("docker-compose build")
            sudo("docker-compose kill django")
            sudo("docker-compose rm -f django")
            sudo("docker-compose up -d")
            # sudo("docker-compose run django python manage.py collectstatic --noinput")
            # sudo("docker-compose run django python manage.py migrate --noinput")

def deploy_staging():
    with settings(user="root", password=password):
        with cd("/root/pyconng"):
            run("pwd")
            run("git branch --set-upstream-to=origin/cfp cfp")
            run("git pull")
            sudo("docker-compose -f dev.yml build django2")
            sudo("docker-compose -f dev.yml up -d django2")

def deploy_current():
    print("hello World")
    run("pwd")
    code_dir = f'/home/{username}/pyconng'
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
