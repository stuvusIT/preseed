#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from string import Template
from sys import exit
from time import sleep
import config as cfg
import subprocess
import socket

remote_ip = ''
machine_config = None

class HttpHandler(BaseHTTPRequestHandler):
    # Do not log, please
    def log_message(self, format, *args):
        return

    def do_GET(self):
        global remote_ip
        global machine_config
        # Verify path
        if self.path != '/d-i/' + cfg.release + '/preseed.cfg':
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('File not found\n')
            print('Invalid request for ' + self.path + ' from ' + self.client_address[0])
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # Template and send configuration
        with open('preseeds/' + cfg.preseed + '.cfg', 'r') as raw:
            template = Template(raw.read())
            self.wfile.write(template.substitute(machine_config))

        remote_ip = self.client_address[0]

def run_in_ansible_home(args):
    return subprocess.Popen(args, stdout=subprocess.PIPE, cwd=cfg.ansible_home).communicate()[0]

def get_ansible_value(name):
    ret = run_in_ansible_home([ 'ansible', 'localhost', '-m', 'debug', '-a', 'msg={{ ' + name + ' }}' ])
    for line in ret.split('\n'):
        if '"msg"' in line:
            return line.split('"')[3]

if __name__ == "__main__":
    # Parse playbook values
    machine_config = cfg.machine_config
    # TODO machine_config.username = get_ansible_value('ansible_user')

    # HTTP server
    addr = ('', cfg.port)
    http_server = HTTPServer(addr, HttpHandler)
    print('Waiting for HTTP connections on port ' + str(cfg.port))
    while remote_ip == '':
        http_server.handle_request()
    print('Sent preseed file to ' + remote_ip)
    print('It is now safe to modify the configuration file and provision another host')

    # Wait for SSH
    print('Waiting for SSH to become available')
    sock = socket.socket()
    while True:
        sleep(10)
        try:
            sock.connect((remote_ip, 22))
        except socket.timeout, err:
            continue
        except socket.error, err:
            continue
        else:
            s.close()
            break
