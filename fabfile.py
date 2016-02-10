from fabric.api import env, run, cd, sudo
from fabric.api import task
import os, json

REGION = os.environ.get("AWS_EC2_REGION")
USER = os.environ.get("AWS_USER")
env.user = USER
env.key_filename = [os.environ.get("ESIP_BADGE_DEV_KEY")]


@task
def set_host():
    env.hosts = [os.environ.get('ESIP_BADGE_EC2_PUBLIC_DNS')]


@task
def deploy_badger(branch=""):
    """update the local repo from master or a branch"""
    with cd("/home/%s/esip_badger" % USER):
        run('git pull origin %s' % branch)


@task
def restart():
    """restart the app"""
    # restart gunicorn
    sudo('badger restart')

    # restart nginx
    sudo('service nginx restart')


@task
def add_term(short_name, long_name, color):
    """
    add a new term

        :short_name = the key used in the URL
        :long_name = the string for the right side of the badge
        :color = hex color for the right side
    """
    with open('badge_term.json', 'r') as f:
        badges = json.loads(f.read())

    if short_name in badges.keys():
        return

    badges[short_name] = {"background": color, "text": long_name}

    with open('badge_term.json', 'w') as f:
        f.write(json.dumps(badges, indent=4))
