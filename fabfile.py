import os
from fabric.api import local, run, cd, env, sudo, settings, lcd
from fabric.decorators import hosts
env.hosts = ['pycon@104.236.214.189']

password = os.getenv('PRODUCTION_PASSWORD', '')


def common_code(code_dir):
    with settings(user="pycon", password=password):
        with cd(code_dir):
            run("pwd")
            run("git pull")
            sudo("docker-compose up -d")


def deploy_current():
    print("hello World")
    run("pwd")
    code_dir = '/home/pycon/pyconng'
    common_code(code_dir)

