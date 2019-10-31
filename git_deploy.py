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
# x don't crash when git pull throws an error (or just use git stash first)
# - validate whether post request is actually from Github
# - more security measures?

import socket
import json
import subprocess
import logging
import conf

HOST = conf.local_ip          # local IP address of server.
PORT = conf.local_port        # Port to listen on.

# Keep dictionary of my git repos and their paths on the pi.
directories = {
    "misc_scripts": "/home/pi/misc_scripts",
    "uw-stroom": "/home/pi/uw-stroom",
    "groupify": "/var/www/groupify",
    "gustav": "/var/www/gustav"
}


def deploy(repo):
    """
    Git pull from the right directory in a subprocess.
    """
    dir = directories[repo]
    command = ['git stash clear && git pull']
    output = subprocess.check_output('git stash; git pull', cwd=dir, shell=True)
    logging.info(output)

def server():
    """
    Listen to certain port that my router forwards, by using some python
    socket programming.
    """

    # Outer while True loop is to keep process running after each connection.
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            logging.info('Waiting for next connection')

            # set address as reusable.
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            content = ''

            # When an IP address binds to the port.
            with conn:
                logging.info('Connected by', addr)
                # Inner while True in order to receive all data.
                while True:
                    data = conn.recv(1024).decode('utf-8')

                    # As long as we keep receiving data, append it.
                    if data:
                        content += data

                    # If no more data is received, start parsing it.
                    else:
                        payload = content.split('\r\n\r\n')[1]
                        payload = json.loads(payload)
                        branch = payload['ref'].split('/')[2]
                        repo = payload['repository']['name']

                        # Only deploy if it was a push to the master.
                        if (branch == 'master'):
                            deploy(repo)

                        # Empty variable and close connection.
                        content = ''
                        s.close()
                        logging.info('Closed connection', addr)
                        break

def main():
    logging.basicConfig(filename='logs/git_deploy.log',
                        level=logging.INFO,
                        format='%(asctime)s :: %(levelname)s :: %(message)s')
    server()

main()
