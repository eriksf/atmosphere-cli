from .mock_server import get_free_port, start_mock_server
from atmosphere.api import AtmosphereAPI
from atmosphere.main import AtmosphereApp
from atmosphere.identity import IdentityList


class TestIdentities(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_users_base_url = 'http://localhost:{port}'.format(port=cls.mock_server_port)
        cls.mock_users_bad_base_url = 'http://localhosty:{port}'.format(port=cls.mock_server_port)
        start_mock_server(cls.mock_server_port)

    def test_identity_list_description(self):
        app = AtmosphereApp()
        identity_list = IdentityList(app, None)
        assert identity_list.get_description() == 'List user identities managed by Atmosphere.'

    def test_getting_identities_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_identities()
        assert not response.ok

    def test_getting_identities_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_identities()
        assert response.ok
        assert response.message['results'][0]['user']['id'] == 1010 and response.message['results'][0]['quota']['cpu'] == 132

    def test_getting_identity_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_identity("32e3354c-03cc-40e1-8c33-02bc7f6be299")
        assert not response.ok

    def test_getting_identity_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_identity("32e3354c-03cc-40e1-8c33-02bc7f6be299")
        assert response.ok
        assert response.message['id'] == 1403 and response.message['quota']['cpu'] == 132
