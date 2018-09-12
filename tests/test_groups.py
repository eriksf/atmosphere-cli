from .mock_server import get_free_port, start_mock_server
from atmosphere.api import AtmosphereAPI
from atmosphere.main import AtmosphereApp
from atmosphere.group import GroupList


class TestGroups(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_users_base_url = 'http://localhost:{port}'.format(port=cls.mock_server_port)
        cls.mock_users_bad_base_url = 'http://localhosty:{port}'.format(port=cls.mock_server_port)
        start_mock_server(cls.mock_server_port)

    def test_group_list_description(self):
        app = AtmosphereApp()
        group_list = GroupList(app, None)
        assert group_list.get_description() == 'List groups for a user.'

    def test_getting_groups_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_groups()
        assert not response.ok

    def test_getting_groups_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_groups()
        assert response.ok
        assert response.message['count'] == 1 and response.message['results'][0]['name'] == 'eriksf'

    def test_getting_group_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_group(2)
        assert not response.ok

    def test_getting_group_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_group(718)
        assert response.ok
        assert response.message['id'] == 718 and response.message['name'] == 'eriksf'
