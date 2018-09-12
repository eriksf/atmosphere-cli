import json
from .mock_server import get_free_port, start_mock_server
from atmosphere.api import AtmosphereAPI
from atmosphere.main import AtmosphereApp
from atmosphere.project import ProjectList


class TestProjects(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_users_base_url = 'http://localhost:{port}'.format(port=cls.mock_server_port)
        cls.mock_users_bad_base_url = 'http://localhosty:{port}'.format(port=cls.mock_server_port)
        start_mock_server(cls.mock_server_port)

    def test_project_list_description(self):
        app = AtmosphereApp()
        project_list = ProjectList(app, None)
        assert project_list.get_description() == 'List projects for a user.'

    def test_getting_projects_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_projects()
        assert not response.ok

    def test_getting_projects_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_projects()
        assert response.ok
        assert response.message['count'] == 2 and response.message['results'][0]['name'] == 'myfirstproject'

    def test_getting_project_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_project(2)
        assert not response.ok

    def test_getting_project_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_project(2)
        assert response.ok
        assert response.message['id'] == 2 and response.message['name'] == 'myfirstproject'

    def test_creating_project_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        payload = {
            'name': '',
            'description': 'my first project',
            'owner': 'eriksf'
        }
        response = api.create_project(json.dumps(payload))
        assert not response.ok
        assert response.message['name'][0] == 'This field may not be blank.'

    def test_creating_project_when_owner_is_invalid(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        payload = {
            'name': 'myfirstproject',
            'description': 'my first project',
            'owner': 'xxxxx'
        }
        response = api.create_project(json.dumps(payload))
        assert not response.ok
        assert response.message['owner'][0] == "Group with Field: name 'xxxxx' does not exist."

    def test_creating_project_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        payload = {
            'name': 'myfirstproject',
            'description': 'my first project',
            'owner': 'eriksf'
        }
        response = api.create_project(json.dumps(payload))
        assert response.ok
        assert response.message['id'] == 2 and response.message['name'] == 'myfirstproject'
