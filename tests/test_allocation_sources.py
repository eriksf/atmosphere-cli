from .mock_server import get_free_port, start_mock_server
from atmosphere.api import AtmosphereAPI
from atmosphere.main import AtmosphereApp
from atmosphere.allocation_source import AllocationSourceList


class TestAllocationSources(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_users_base_url = 'http://localhost:{port}'.format(port=cls.mock_server_port)
        cls.mock_users_bad_base_url = 'http://localhosty:{port}'.format(port=cls.mock_server_port)
        start_mock_server(cls.mock_server_port)

    def test_allocation_source_list_description(self):
        app = AtmosphereApp()
        allocation_source_list = AllocationSourceList(app, None)
        assert allocation_source_list.get_description() == 'List allocation sources for a user.'

    def test_getting_allocation_sources_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_allocation_sources()
        assert not response.ok

    def test_getting_allocation_sources_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_allocation_sources()
        assert response.ok
        assert response.message['results'][0]['id'] == 1 and response.message['results'][0]['name'] == 'eriksf'

    def test_getting_allocation_source_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_allocation_source(1)
        assert not response.ok

    def test_getting_allocation_source_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_allocation_source(1)
        assert response.ok
        assert response.message['id'] == 1 and response.message['name'] == 'eriksf'
