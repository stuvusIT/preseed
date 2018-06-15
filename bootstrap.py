#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from string import Template
from sys import exit
import config as cfg
import socket

remote_ip = ''

class HttpHandler(BaseHTTPRequestHandler):
    # Do not log, please
    def log_message(self, format, *args):
        return

    def do_GET(self):
        global remote_ip
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
            self.wfile.write(template.substitute(cfg.machine_config))

        remote_ip = self.client_address[0]


if __name__ == "__main__":
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
        try:
            sock.connect((remote_ip, 22))
        except socket.timeout, err:
            continue
        except socket.error, err:
            continue
        else:
            s.close()
            break
