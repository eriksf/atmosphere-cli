from mock_server import get_free_port, start_mock_server
from atmosphere.api import AtmosphereAPI


class TestIdentities(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_users_base_url = 'http://localhost:{port}'.format(port=cls.mock_server_port)
        cls.mock_users_bad_base_url = 'http://localhosty:{port}'.format(port=cls.mock_server_port)
        start_mock_server(cls.mock_server_port)

    def test_getting_identities_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_identities()
        assert not response

    def test_getting_identities_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_identities()
        assert response['results'][0]['user']['id'] == 1 and response['results'][0]['usage']['current'] == 112

    def test_getting_identity_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_identity(1)
        assert not response

    def test_getting_identity_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_identity(1)
        assert response['id'] == 1 and response['usage']['current'] == 112
