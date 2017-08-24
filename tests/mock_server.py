from six.moves import BaseHTTPServer
from six.moves.urllib.parse import urlparse, parse_qs
import os
import re
import socket
from threading import Thread
import time
import requests


class MockServerRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    IDENTITY_PATTERN = re.compile(r'/identities/\d+')
    IDENTITIES_PATTERN = re.compile(r'/identities')
    IMAGE_PATTERN = re.compile(r'/images/\d+')
    IMAGES_PATTERN = re.compile(r'/images')
    INSTANCE_PATTERN = re.compile(r'/instances/\d+')
    INSTANCES_PATTERN = re.compile(r'/instances')
    PROVIDER_PATTERN = re.compile(r'/providers/\d+')
    PROVIDERS_PATTERN = re.compile(r'/providers')
    SIZE_PATTERN = re.compile(r'/sizes/\d+')
    SIZES_PATTERN = re.compile(r'/sizes')
    BAD_JSON_PATTERN = re.compile(r'/badjson')
    VALID_JSON_PATTERN = re.compile(r'/valid')
    TIMEOUT_PATTERN = re.compile(r'/timeout')
    VERSION_PATTERN = re.compile(r'/version')
    RESPONSE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'responses')
    IDENTITY_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'identity.json')
    IDENTITIES_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'identities.json')
    IMAGE_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'image.json')
    IMAGES_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'images.json')
    INSTANCE_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'instance.json')
    INSTANCES_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'instances.json')
    PROVIDER_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'provider.json')
    PROVIDERS_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'providers.json')
    SIZE_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'size.json')
    SIZES_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'sizes.json')
    SIZES_FILTERED_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'sizes_filtered.json')
    VERSION_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'version.json')

    def __send_response(self, content):
        # Add response status code
        self.send_response(requests.codes.ok)
        # Add response headers
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        # Add response content
        self.wfile.write(content.encode('utf-8'))

    def __send_response_file(self, response_file):
        # Add response status code
        self.send_response(requests.codes.ok)
        # Add response headers
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        # Add response content
        with open(response_file) as f: response_content = f.read()
        self.wfile.write(response_content.encode('utf-8'))

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)
        if re.match(self.IDENTITY_PATTERN, self.path):
            self.__send_response_file(self.IDENTITY_RESPONSE_FILE)
            return
        elif re.match(self.IDENTITIES_PATTERN, self.path):
            self.__send_response_file(self.IDENTITIES_RESPONSE_FILE)
            return
        elif re.match(self.IMAGE_PATTERN, self.path):
            self.__send_response_file(self.IMAGE_RESPONSE_FILE)
            return
        elif re.match(self.IMAGES_PATTERN, self.path):
            self.__send_response_file(self.IMAGES_RESPONSE_FILE)
            return
        elif re.match(self.INSTANCE_PATTERN, self.path):
            self.__send_response_file(self.INSTANCE_RESPONSE_FILE)
            return
        elif re.match(self.INSTANCES_PATTERN, self.path):
            self.__send_response_file(self.INSTANCES_RESPONSE_FILE)
            return
        elif re.match(self.PROVIDER_PATTERN, self.path):
            self.__send_response_file(self.PROVIDER_RESPONSE_FILE)
            return
        elif re.match(self.PROVIDERS_PATTERN, self.path):
            self.__send_response_file(self.PROVIDERS_RESPONSE_FILE)
            return
        elif re.match(self.SIZE_PATTERN, self.path):
            self.__send_response_file(self.SIZE_RESPONSE_FILE)
            return
        elif re.match(self.SIZES_PATTERN, self.path):
            if 'provider__id' in query:
                self.__send_response_file(self.SIZES_FILTERED_RESPONSE_FILE)
            else:
                self.__send_response_file(self.SIZES_RESPONSE_FILE)
            return
        elif re.match(self.BAD_JSON_PATTERN, self.path):
            response_content = '{"results": [}'
            self.__send_response(response_content)
            return
        elif re.match(self.VALID_JSON_PATTERN, self.path):
            response_content = '{"results": [], "valid": "TRUE"}'
            self.__send_response(response_content)
            return
        elif re.match(self.TIMEOUT_PATTERN, self.path):
            time.sleep(2)
            response_content = '{"results": []}'
            self.__send_response(response_content)
            return
        elif re.match(self.VERSION_PATTERN, self.path):
            self.__send_response_file(self.VERSION_RESPONSE_FILE)
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
