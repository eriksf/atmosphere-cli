from six.moves import BaseHTTPServer
from six.moves.urllib.parse import urlparse, parse_qs
import json
import os
import re
import socket
from threading import Thread
import time
import requests


class MockServerRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    ALLOCATION_SOURCE_PATTERN = re.compile(r'/allocation_sources/\d+')
    ALLOCATION_SOURCES_PATTERN = re.compile(r'/allocation_sources')
    IDENTITY_PATTERN = re.compile(r'/identities/\d+')
    IDENTITIES_PATTERN = re.compile(r'/identities')
    IMAGE_PATTERN = re.compile(r'/images/\d+')
    IMAGE_VERSION_PATTERN = re.compile(r'/image_versions/\d+')
    IMAGES_PATTERN = re.compile(r'/images')
    INSTANCE_PATTERN = re.compile(r'/instances/\d+')
    INSTANCE_ACTIONS_PATTERN = re.compile(r'/instances/[\d\w-]+/actions')
    INSTANCE_HISTORY_PATTERN = re.compile(r'/instance_histories')
    INSTANCES_PATTERN = re.compile(r'/instances')
    PROJECT_PATTERN = re.compile(r'/projects/\d+')
    PROJECTS_PATTERN = re.compile(r'/projects')
    PROVIDER_PATTERN = re.compile(r'/providers/\d+')
    PROVIDERS_PATTERN = re.compile(r'/providers')
    SIZE_PATTERN = re.compile(r'/sizes/\d+')
    SIZES_PATTERN = re.compile(r'/sizes')
    BAD_JSON_PATTERN = re.compile(r'/badjson')
    VALID_JSON_PATTERN = re.compile(r'/valid')
    TIMEOUT_PATTERN = re.compile(r'/timeout')
    VERSION_PATTERN = re.compile(r'/version')
    VOLUME_PATTERN = re.compile(r'/volumes/\d+')
    VOLUMES_PATTERN = re.compile(r'/volumes')
    TOKENS_PATTERN = re.compile(r'/tokens/[\d\w-]')
    RESPONSE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'responses')
    ALLOCATION_SOURCE_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'allocation_source.json')
    ALLOCATION_SOURCES_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'allocation_sources.json')
    IDENTITY_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'identity.json')
    IDENTITIES_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'identities.json')
    IMAGE_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'image.json')
    IMAGE_VERSION_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'image_version.json')
    IMAGES_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'images.json')
    IMAGES_SEARCH_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'image_search.json')
    IMAGES_FILTERED_TAG_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'images_filtered_tag.json')
    IMAGES_FILTERED_CREATOR_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'images_filtered_creator.json')
    INSTANCE_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'instance.json')
    INSTANCE_ACTIONS_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'instance_actions.json')
    INSTANCE_CREATED_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'instance_created.json')
    INSTANCES_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'instances.json')
    INSTANCE_SUSPENDED_FILE = os.path.join(RESPONSE_DIR, 'instance_suspended.json')
    INSTANCE_RESUMED_FILE = os.path.join(RESPONSE_DIR, 'instance_resumed.json')
    INSTANCE_STARTED_FILE = os.path.join(RESPONSE_DIR, 'instance_started.json')
    INSTANCE_STOPPED_FILE = os.path.join(RESPONSE_DIR, 'instance_stopped.json')
    INSTANCE_REBOOTED_FILE = os.path.join(RESPONSE_DIR, 'instance_rebooted.json')
    INSTANCE_REDEPLOYED_FILE = os.path.join(RESPONSE_DIR, 'instance_redeployed.json')
    INSTANCE_SHELVED_FILE = os.path.join(RESPONSE_DIR, 'instance_shelved.json')
    INSTANCE_UNSHELVED_FILE = os.path.join(RESPONSE_DIR, 'instance_unshelved.json')
    INSTANCE_HISTORY_FILE = os.path.join(RESPONSE_DIR, 'instance_history.json')
    INSTANCE_ATTACHED_VOLUME_FILE = os.path.join(RESPONSE_DIR, 'instance_attached_volume.json')
    INSTANCE_DETACHED_VOLUME_FILE = os.path.join(RESPONSE_DIR, 'instance_detached_volume.json')
    PROJECT_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'project.json')
    PROJECT_CREATED_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'project_created.json')
    PROJECTS_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'projects.json')
    PROVIDER_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'provider.json')
    PROVIDERS_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'providers.json')
    SIZE_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'size.json')
    SIZES_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'sizes.json')
    SIZES_FILTERED_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'sizes_filtered.json')
    VERSION_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'version.json')
    VOLUME_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'volume.json')
    VOLUME_CREATED_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'volume_created.json')
    VOLUMES_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'volumes.json')
    TOKENS_RESPONSE_FILE = os.path.join(RESPONSE_DIR, 'tokens.json')

    def __send_response(self, content):
        # Add response status code
        self.send_response(requests.codes.ok)
        # Add response headers
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        # Add response content
        self.wfile.write(content.encode('utf-8'))

    def __send_no_content_response(self):
        # Add response status code
        self.send_response(requests.codes.no_content)
        self.end_headers()

    def __send_error_response(self, error_status_code, content):
        # Add response status code
        # self.send_response(error_status_code)
        self.send_response(requests.codes.bad_request)
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

    def do_DELETE(self):
        if re.match(self.VOLUME_PATTERN, self.path):
            self.__send_no_content_response()
        return

    def do_POST(self):
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(data_string)
        if re.match(self.PROJECTS_PATTERN, self.path):
            if data['name'] == '':
                self.__send_error_response(requests.codes.bad_request, '{"name":["This field may not be blank."]}')
            else:
                self.__send_response_file(self.PROJECT_CREATED_RESPONSE_FILE)
        elif re.match(self.INSTANCE_ACTIONS_PATTERN, self.path):
            action = data['action']
            if action == 'suspend':
                self.__send_response_file(self.INSTANCE_SUSPENDED_FILE)
            elif action == 'resume':
                self.__send_response_file(self.INSTANCE_RESUMED_FILE)
            elif action == 'start':
                self.__send_response_file(self.INSTANCE_STARTED_FILE)
            elif action == 'stop':
                self.__send_response_file(self.INSTANCE_STOPPED_FILE)
            elif action == 'reboot':
                self.__send_response_file(self.INSTANCE_REBOOTED_FILE)
            elif action == 'redeploy':
                self.__send_response_file(self.INSTANCE_REDEPLOYED_FILE)
            elif action == 'shelve':
                self.__send_response_file(self.INSTANCE_SHELVED_FILE)
            elif action == 'unshelve':
                self.__send_response_file(self.INSTANCE_UNSHELVED_FILE)
            elif action == 'attach_volume':
                self.__send_response_file(self.INSTANCE_ATTACHED_VOLUME_FILE)
            elif action == 'detach_volume':
                self.__send_response_file(self.INSTANCE_DETACHED_VOLUME_FILE)
        elif re.match(self.INSTANCES_PATTERN, self.path):
            if 'allocation_source_id' not in data:
                print('error')
                self.__send_error_response(requests.codes.bad_request, '{"errors":[{"code": 400, "message":{"allocation_source_id":"This field is required."}}]}')
            else:
                self.__send_response_file(self.INSTANCE_CREATED_RESPONSE_FILE)
        elif re.match(self.VOLUMES_PATTERN, self.path):
            if data['name'] == '':
                self.__send_error_response(requests.codes.bad_request, '{"name":["This field may not be blank."]}')
            else:
                self.__send_response_file(self.VOLUME_CREATED_RESPONSE_FILE)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)
        if re.match(self.ALLOCATION_SOURCE_PATTERN, self.path):
            self.__send_response_file(self.ALLOCATION_SOURCE_RESPONSE_FILE)
            return
        elif re.match(self.ALLOCATION_SOURCES_PATTERN, self.path):
            self.__send_response_file(self.ALLOCATION_SOURCES_RESPONSE_FILE)
            return
        elif re.match(self.IDENTITY_PATTERN, self.path):
            self.__send_response_file(self.IDENTITY_RESPONSE_FILE)
            return
        elif re.match(self.IDENTITIES_PATTERN, self.path):
            self.__send_response_file(self.IDENTITIES_RESPONSE_FILE)
            return
        elif re.match(self.IMAGE_PATTERN, self.path):
            self.__send_response_file(self.IMAGE_RESPONSE_FILE)
            return
        elif re.match(self.IMAGES_PATTERN, self.path):
            if 'tag_name' in query:
                self.__send_response_file(self.IMAGES_FILTERED_TAG_RESPONSE_FILE)
            elif 'created_by' in query:
                self.__send_response_file(self.IMAGES_FILTERED_CREATOR_RESPONSE_FILE)
            elif 'search' in query:
                self.__send_response_file(self.IMAGES_SEARCH_RESPONSE_FILE)
            else:
                self.__send_response_file(self.IMAGES_RESPONSE_FILE)
            return
        elif re.match(self.IMAGE_VERSION_PATTERN, self.path):
            self.__send_response_file(self.IMAGE_VERSION_RESPONSE_FILE)
            return
        elif re.match(self.INSTANCE_ACTIONS_PATTERN, self.path):
            self.__send_response_file(self.INSTANCE_ACTIONS_RESPONSE_FILE)
            return
        elif re.match(self.INSTANCE_HISTORY_PATTERN, self.path):
            self.__send_response_file(self.INSTANCE_HISTORY_FILE)
            return
        elif re.match(self.INSTANCE_PATTERN, self.path):
            self.__send_response_file(self.INSTANCE_RESPONSE_FILE)
            return
        elif re.match(self.INSTANCES_PATTERN, self.path):
            self.__send_response_file(self.INSTANCES_RESPONSE_FILE)
            return
        elif re.match(self.PROJECT_PATTERN, self.path):
            self.__send_response_file(self.PROJECT_RESPONSE_FILE)
            return
        elif re.match(self.PROJECTS_PATTERN, self.path):
            self.__send_response_file(self.PROJECTS_RESPONSE_FILE)
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
        elif re.match(self.VOLUME_PATTERN, self.path):
            self.__send_response_file(self.VOLUME_RESPONSE_FILE)
            return
        elif re.match(self.VOLUMES_PATTERN, self.path):
            self.__send_response_file(self.VOLUMES_RESPONSE_FILE)
            return
        elif re.match(self.TOKENS_PATTERN, self.path):
            self.__send_response_file(self.TOKENS_RESPONSE_FILE)
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
