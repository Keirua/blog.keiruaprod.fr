from fabric.api import *
from fabric.contrib.files import exists
from fabric.contrib.project import *
from time import time
from datetime import datetime
from sys import exit

env.hosts = [
    'ssh.cluster003.ovh.net'
]
env.user = 'keiruapr'

def deploy():
    deploy_timestamp = datetime.utcfromtimestamp(int(time())).strftime('%Y-%b-%d-at-%H:%M:%S')

    deployment_directory='/homez.57/keiruapr/blog/releases/release-%s' % (deploy_timestamp)
    
    upload_code(deployment_directory)
    enable_new_version( deployment_directory)

def upload_code(deployment_directory):
    if not exists(deployment_directory):
       puts('creating deployment directory')
       run('mkdir -p %s' % deployment_directory) 

    puts('Deploying project in %s' % deployment_directory)
    rsync_project(
        local_dir='./_site/*',
        remote_dir=deployment_directory,
        default_opts='-azcrSh --stats',
        exclude=['.git', 'var', 'node_modules', 'vendor', 'UNLICENSE.txt', 'README.md'],
    )

def enable_new_version(deployment_directory):
    # Create symlink
    run('ln -sfn %s /homez.57/keiruapr/blog/www' % (deployment_directory))
    pass

