import logging
from .mock_server import get_free_port, start_mock_server
from atmosphere.api.request import Request


log = logging.getLogger('atmosphere.api.request')
log.setLevel(logging.DEBUG)


class TestRequest(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_users_base_url = 'http://localhost:{port}'.format(port=cls.mock_server_port)
        cls.mock_users_bad_base_url = 'http://localhosty:{port}'.format(port=cls.mock_server_port)
        start_mock_server(cls.mock_server_port)

    def test_request_when_url_is_unknown(self):
        req = Request('token', self.mock_users_base_url, None, True)
        data = req.getJson('GET', 'http://my.example.com')
        assert not data.ok

    def test_request_when_verb_is_unsupported(self):
        req = Request('token', self.mock_users_base_url, None, True)
        data = req.getJson('DELETE', '/images/1')
        assert not data.ok

    def test_request_when_returns_invalid_json(self):
        req = Request('token', self.mock_users_base_url, None, True)
        data = req.getJson('GET', '/badjson')
        assert not data.ok

    def test_request_when_exceeds_timeout(self):
        req = Request('token', self.mock_users_base_url, 1, True)
        data = req.getJson('GET', '/timeout')
        assert not data.ok

    def test_request_when_return_is_valid_json(self):
        req = Request('token', self.mock_users_base_url, None, True)
        data = req.getJson('GET', '/valid')
        assert data.ok and data.message['valid']
