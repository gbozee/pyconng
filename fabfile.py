import os
from fabric.api import local, run, cd, env, sudo, settings, lcd
from fabric.decorators import hosts
env.hosts = ['pycon@www.pycon.ng']

password = os.getenv('PRODUCTION_PASSWORD', '')


def common_code(code_dir):
    with settings(user="pycon", password=password):
        with cd(code_dir):
            sudo("pwd")
            sudo("git pull")
            sudo("docker-compose up -d")


def deploy_current():
    print("hello World")
    run("pwd")
    code_dir = '/home/pycon/pyconng'
    common_code(code_dir)

