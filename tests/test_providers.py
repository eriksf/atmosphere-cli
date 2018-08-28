from .mock_server import get_free_port, start_mock_server
from atmosphere.api import AtmosphereAPI
from atmosphere.main import AtmosphereApp
from atmosphere.provider import ProviderList


class TestProviders(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_users_base_url = 'http://localhost:{port}'.format(port=cls.mock_server_port)
        cls.mock_users_bad_base_url = 'http://localhosty:{port}'.format(port=cls.mock_server_port)
        start_mock_server(cls.mock_server_port)

    def test_provider_list_description(self):
        app = AtmosphereApp()
        provider_list = ProviderList(app, None)
        assert provider_list.get_description() == 'List cloud providers managed by Atmosphere.'

    def test_getting_providers_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_providers()
        assert not response.ok

    def test_getting_providers_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_providers()
        assert response.ok
        assert response.message['count'] == 1 and response.message['results'][0]['name'] == 'Cloudlab - ErikOS'

    def test_getting_provider_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_provider(4)
        assert not response.ok

    def test_getting_provider_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_provider(4)
        assert response.ok
        assert response.message['id'] == 4 and response.message['name'] == 'Cloudlab - ErikOS'
