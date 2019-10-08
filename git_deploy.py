#!/usr/bin/env python3

# git_deploy.py
# Small python program running as daemon on server that makes deployment over
# git possible. Using the post request sent by the git webhook, it pulls from
# the right directory.
#
# TODO:
# x leave server idle after succesful connection
# x log connections
# - validate whether post request is actually from Github
# - more security measures?

import socket
import sys
import json
import subprocess
import conf
import time

HOST = conf.local_ip          # local IP address of server
PORT = conf.local_port        # Port to listen on (non-privileged ports are > 1023)

directories = {
    "misc_scripts": "/home/pi/misc_scripts",
    "uw-stroom": "/home/pi/uw-stroom"
}

def deploy(repo):
    dir = directories[repo]
    # subprocess.check_call when in production.
    output = subprocess.check_output(['git', 'pull'], cwd=dir)

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Waiting for next connection')

        # set address as reusable.
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        content = ''

        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024).decode('utf-8')

                if data:
                    content += data

                else:
                    payload = content.split('\r\n\r\n')[1]
                    payload = json.loads(payload)
                    branch = payload['ref'].split('/')[2]
                    repo = payload['repository']['name']

                    if (branch == 'master'):
                        deploy(repo)

                    content = ''
                    s.close()
                    print('Closed connection', addr)
                    break
