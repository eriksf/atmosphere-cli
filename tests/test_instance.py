import json
from mock_server import get_free_port, start_mock_server
from atmosphere.api import AtmosphereAPI
from atmosphere.main import AtmosphereApp
from atmosphere.instance import InstanceList


class TestInstances(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_users_base_url = 'http://localhost:{port}'.format(port=cls.mock_server_port)
        cls.mock_users_bad_base_url = 'http://localhosty:{port}'.format(port=cls.mock_server_port)
        start_mock_server(cls.mock_server_port)

    def test_instance_list_description(self):
        app = AtmosphereApp()
        instance_list = InstanceList(app, None)
        assert instance_list.get_description() == 'List instances for user.'

    def test_getting_instances_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_instances()
        assert not response

    def test_getting_instances_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_instances()
        assert response['count'] == 1 and response['results'][0]['name'] == 'trusty-server'

    def test_getting_instance_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_instance(1)
        assert not response

    def test_getting_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_instance(1)
        assert response['id'] == 1 and response['name'] == 'trusty-server'

    def test_getting_instance_actions_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_instance_actions(1)
        assert not response

    def test_getting_instance_actions_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_instance_actions(1)
        print(response)
        assert response[4]['key'] == 'Reboot' and response[4]['description'] == 'Reboots an instance when it is in ANY State'

    def test_creating_instance_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        payload = {
            "identity": "a5a6140d-1122-4581-87dc-bd9704fa07ec",
            "name": "myfirstinstance",
            "project": "7c8d34b1-1b2d-4f7f-bd62-4e0929295fd4",
            "size_alias": "100",
            "source_alias": "ec4fb434-a7b7-4c57-b882-0a1bf34506df",
            "scripts": [],
            "deploy": True,
            "extra": {}
        }
        response = api.create_instance(json.dumps(payload))
        assert response['errors'][0]['message']['allocation_source_id'] == 'This field is required.'

    def test_creating_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        payload = {
            "identity": "a5a6140d-1122-4581-87dc-bd9704fa07ec",
            "name": "myfirstinstance",
            "project": "7c8d34b1-1b2d-4f7f-bd62-4e0929295fd4",
            "size_alias": "100",
            "source_alias": "ec4fb434-a7b7-4c57-b882-0a1bf34506df",
            "allocation_source_id": "f4cca788-e039-4f82-bc77-9fb92141eca6",
            "scripts": [],
            "deploy": True,
            "extra": {}
        }
        response = api.create_instance(json.dumps(payload))
        assert response['id'] == 1 and response['name'] == 'myfirstinstance'
