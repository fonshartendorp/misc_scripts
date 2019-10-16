#!/usr/bin/env python3

# git_deploy.py
# Small python program running as daemon on my raspberry pi server that makes
# deployment over git possible. Using the post request sent by the git
# webhook, it pulls from the right directory.
#
# TODO:
# x leave server idle after succesful connection
# x log connections
# - send reply back to github server
# - don't crash when git pull throws an error (or just use git stash first)
# - validate whether post request is actually from Github
# - more security measures?

import socket
import json
import subprocess
import conf

HOST = conf.local_ip          # local IP address of server.
PORT = conf.local_port        # Port to listen on.

# Keep dict of my git repos and their paths on the pi.
directories = {
    "misc_scripts": "/home/pi/misc_scripts",
    "uw-stroom": "/home/pi/uw-stroom"
}


def deploy(repo):
    """
    Git pull from the right directory in a subprocess.
    """
    dir = directories[repo]
    command = ['git stash clear && git pull']
    # subprocess.check_call when in production.
    output = subprocess.check_output(command, cwd=dir)

    # output = subprocess.check_output(['git', 'stash', 'clear', '&&', 'git', 'pull'], cwd=dir)

def server():
    """
    Listen to certain port that my router forwards, by using some python
    socket programming.
    """
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

server()
