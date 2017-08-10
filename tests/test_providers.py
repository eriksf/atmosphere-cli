from mock_server import get_free_port, start_mock_server
from atmosphere.api import AtmosphereAPI


class TestProviders(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_users_base_url = 'http://localhost:{port}'.format(port=cls.mock_server_port)
        cls.mock_users_bad_base_url = 'http://localhosty:{port}'.format(port=cls.mock_server_port)
        start_mock_server(cls.mock_server_port)

    def test_getting_providers_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_providers()
        assert not response

    def test_getting_providers_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_providers()
        assert response['results'][0]['name'] == 'iPlant Cloud - Tucson'

    def test_getting_provider_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_provider(4)
        assert not response

    def test_getting_provider_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_provider(4)
        assert response['id'] == 4 and response['name'] == 'iPlant Cloud - Tucson'
