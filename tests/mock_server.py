from six.moves import BaseHTTPServer
import os
import re
import socket
from threading import Thread
import time
import requests


class MockServerRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    IMAGE_PATTERN = re.compile(r'/images/\d+')
    IMAGES_PATTERN = re.compile(r'/images')
    PROVIDER_PATTERN = re.compile(r'/providers/\d+')
    PROVIDERS_PATTERN = re.compile(r'/providers')
    BAD_JSON_PATTERN = re.compile(r'/badjson')
    VALID_JSON_PATTERN = re.compile(r'/valid')
    TIMEOUT_PATTERN = re.compile(r'/timeout')
    RESPONSE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'responses')
    IMAGE_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'image.json')
    IMAGES_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'images.json')
    PROVIDER_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'provider.json')
    PROVIDERS_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'providers.json')

    def do_GET(self):
        if re.match(self.IMAGE_PATTERN, self.path):
            # Add response status code
            self.send_response(requests.codes.ok)
            # Add response headers
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            # Add response content
            with open(self.IMAGE_RESPONSE_FILE) as f: response_content = f.read()
            self.wfile.write(response_content.encode('utf-8'))
            return
        elif re.match(self.IMAGES_PATTERN, self.path):
            # Add response status code
            self.send_response(requests.codes.ok)
            # Add response headers
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            # Add response content
            with open(self.IMAGES_RESPONSE_FILE) as f: response_content = f.read()
            self.wfile.write(response_content.encode('utf-8'))
            return
        elif re.match(self.PROVIDER_PATTERN, self.path):
            # Add response status code
            self.send_response(requests.codes.ok)
            # Add response headers
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            # Add response content
            with open(self.PROVIDER_RESPONSE_FILE) as f: response_content = f.read()
            self.wfile.write(response_content.encode('utf-8'))
            return
        elif re.match(self.PROVIDERS_PATTERN, self.path):
            # Add response status code
            self.send_response(requests.codes.ok)
            # Add response headers
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            # Add response content
            with open(self.PROVIDERS_RESPONSE_FILE) as f: response_content = f.read()
            self.wfile.write(response_content.encode('utf-8'))
            return
        elif re.match(self.BAD_JSON_PATTERN, self.path):
            # Add response status code
            self.send_response(requests.codes.ok)
            # Add response headers
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            # Add response content
            response_content = '{"results": [}'
            self.wfile.write(response_content.encode('utf-8'))
            return
        elif re.match(self.VALID_JSON_PATTERN, self.path):
            # Add response status code
            self.send_response(requests.codes.ok)
            # Add response headers
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            # Add response content
            response_content = '{"results": [], "valid": "TRUE"}'
            self.wfile.write(response_content.encode('utf-8'))
            return
        elif re.match(self.TIMEOUT_PATTERN, self.path):
            time.sleep(2)
            # Add response status code
            self.send_response(requests.codes.ok)
            # Add response headers
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            # Add response content
            response_content = '{"results": []}'
            self.wfile.write(response_content.encode('utf-8'))
            return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port):
    mock_server = BaseHTTPServer.HTTPServer(('localhost', port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()
