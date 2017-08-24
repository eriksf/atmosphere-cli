from mock_server import get_free_port, start_mock_server
from atmosphere.api import AtmosphereAPI
from atmosphere.main import AtmosphereApp
from atmosphere.size import SizeList


class TestSizes(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_users_base_url = 'http://localhost:{port}'.format(port=cls.mock_server_port)
        cls.mock_users_bad_base_url = 'http://localhosty:{port}'.format(port=cls.mock_server_port)
        start_mock_server(cls.mock_server_port)

    def test_size_list_description(self):
        app = AtmosphereApp()
        size_list = SizeList(app, None)
        assert size_list.get_description() == 'List sizes (instance configurations) for cloud provider.'

    def test_getting_sizes_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_sizes()
        assert not response

    def test_getting_sizes_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_sizes()
        assert response['count'] == 1 and response['results'][0]['name'] == 'small1'

    def test_getting_sizes_when_response_is_ok_and_filtering_on_provider(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_sizes(provider_id=2)
        assert response['count'] == 0 and len(response['results']) == 0

    def test_getting_size_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_size(1)
        assert not response

    def test_getting_size_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_size(1)
        assert response['id'] == 1 and response['cpu'] == 2
