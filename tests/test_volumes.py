from mock_server import get_free_port, start_mock_server
from atmosphere.api import AtmosphereAPI
from atmosphere.main import AtmosphereApp
from atmosphere.volume import VolumeList


class Testvolumes(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_users_base_url = 'http://localhost:{port}'.format(port=cls.mock_server_port)
        cls.mock_users_bad_base_url = 'http://localhosty:{port}'.format(port=cls.mock_server_port)
        start_mock_server(cls.mock_server_port)

    def test_volume_list_description(self):
        app = AtmosphereApp()
        volume_list = VolumeList(app, None)
        assert volume_list.get_description() == 'List volumes for a user.'

    def test_getting_volumes_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_volumes()
        assert not response

    def test_getting_volumes_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_volumes()
        assert response['count'] == 1 and response['results'][0]['name'] == 'myfirstvolume'

    def test_getting_volume_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_volume(1)
        assert not response

    def test_getting_volume_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_volume(1)
        assert response['id'] == 1 and response['name'] == 'myfirstvolume'
