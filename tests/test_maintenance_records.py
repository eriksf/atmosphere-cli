from .mock_server import get_free_port, start_mock_server
from atmosphere.api import AtmosphereAPI
from atmosphere.main import AtmosphereApp
from atmosphere.maintenance_record import MaintenanceRecordList


class TestMaintenanceRecords(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_users_base_url = 'http://localhost:{port}'.format(port=cls.mock_server_port)
        cls.mock_users_bad_base_url = 'http://localhosty:{port}'.format(port=cls.mock_server_port)
        start_mock_server(cls.mock_server_port)

    def test_maintenance_record_list_description(self):
        app = AtmosphereApp()
        maintenance_record_list = MaintenanceRecordList(app, None)
        assert maintenance_record_list.get_description() == 'List maintenance records for Atmosphere.'

    def test_getting_maintenance_records_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_maintenance_records()
        assert not response.ok

    def test_getting_maintenance_records_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_maintenance_records()
        assert response.ok
        assert response.message['count'] == 0 and len(response.message['results']) == 0

    def test_getting_maintenance_records_when_response_is_ok_and_showing_all_records(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_maintenance_records(show_all=True)
        assert response.ok
        assert response.message['count'] == 18 and response.message['results'][0]['title'] == '8/14/18 - v33 deployment'

    def test_getting_maintenance_record_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_maintenance_record(19)
        assert not response.ok

    def test_getting_maintenance_record_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_maintenance_record(19)
        assert response.ok
        assert response.message['id'] == 19 and response.message['title'] == '8/14/18 - v33 deployment'
