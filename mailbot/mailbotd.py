#!/usr/bin/env python

import sys
import email
import http.server

from mailbot import mailbot

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(405)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("This operation is currently unsupported")

    def do_GET(self):
        self.send_response(405)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("This operation is currently unsupported")

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        args = mailbot.parseArgs([])
        #mailbot.send_mail(args)

        self.wfile.write("Email sent!\n".encode())

    def populate_namespace_from_headers(self, namespace, headers):
        namespace.to = headers.get('to')

def keep_running():
    return True

def main(args=sys.argv[1:]):
    server_address = ('', 8080)
    httpd = http.server.HTTPServer(server_address, MyHandler)
    while keep_running():
        httpd.handle_request()

if __name__ == '__main__':
  main(sys.argv[1:])
