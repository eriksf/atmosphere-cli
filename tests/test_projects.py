import json
from mock_server import get_free_port, start_mock_server
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
        assert not response

    def test_getting_projects_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_projects()
        assert response['count'] == 1 and response['results'][0]['name'] == 'My Project'

    def test_getting_project_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_project(1)
        assert not response

    def test_getting_project_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_project(1)
        assert response['id'] == 1 and response['name'] == 'My Project'

    def test_creating_project_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        payload = {
            'name': '',
            'description': 'another project'
        }
        response = api.create_project(json.dumps(payload))
        assert response['name'][0] == 'This field may not be blank.'

    def test_creating_project_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        payload = {
            'name': 'another project',
            'description': 'another project'
        }
        response = api.create_project(json.dumps(payload))
        assert response['id'] == 2 and response['name'] == 'another project'