import re
from .mock_server import get_free_port, start_mock_server
from atmosphere.api import AtmosphereAPI
from atmosphere.main import AtmosphereApp
from atmosphere.image import ImageList


def is_term_in_image_result(result, term):
    """check if term exists in name, description, or tags"""
    in_name = re.search(term, result['name'], re.IGNORECASE)
    in_description = re.search(term, result['description'], re.IGNORECASE)
    in_tags = [t['name'] for t in result['tags'] if re.search(term, t['name'], re.IGNORECASE) or re.search(term, t['description'], re.IGNORECASE)]
    in_created_by = re.search(term, result['created_by']['username'], re.IGNORECASE)
    return in_name or in_description or in_tags or in_created_by


class TestImages(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_users_base_url = 'http://localhost:{port}'.format(port=cls.mock_server_port)
        cls.mock_users_bad_base_url = 'http://localhosty:{port}'.format(port=cls.mock_server_port)
        start_mock_server(cls.mock_server_port)

    def test_image_list_description(self):
        app = AtmosphereApp()
        image_list = ImageList(app, None)
        assert image_list.get_description() == 'List images for user.'

    def test_getting_images_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_images()
        assert not response.ok

    def test_getting_images_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_images()
        assert response.ok
        assert response.message['count'] == 10 and response.message['results'][0]['name'] == 'Centos 7 (7.4) Development GUI'

    def test_getting_images_when_response_is_ok_and_filtering_on_tag(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_images(tag_name='docker')
        assert response.ok
        results = response.message['results']
        fcount = 0
        for r in results:
            if is_term_in_image_result(r, 'docker'):
                fcount += 1
        assert response.message['count'] == 11 and fcount == 11

    def test_getting_images_when_response_is_ok_and_filtering_on_creator(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_images(created_by='jfischer')
        assert response.ok
        results = response.message['results']
        fcount = 0
        for r in results:
            if is_term_in_image_result(r, 'jfischer'):
                fcount += 1
        assert response.message['count'] == 9 and fcount == 9

    def test_searching_images_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.search_images('galaxy')
        assert response.ok
        results = response.message['results']
        fcount = 0
        for r in results:
            if is_term_in_image_result(r, 'galaxy'):
                fcount += 1
        assert response.message['count'] == 3 and fcount == 3

    def test_getting_image_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_image(1)
        assert not response.ok

    def test_getting_image_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_image(1)
        assert response.ok
        assert response.message['id'] == 55 and response.message['name'] == 'BioLinux 8'

    def test_getting_image_versions_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_image_versions('ca948f10-c47e-5d06-a2b0-1674cfc002ee')
        assert not response.ok

    def test_getting_image_versions_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_image_versions('ca948f10-c47e-5d06-a2b0-1674cfc002ee')
        assert response.ok
        assert response.message['count'] == 5 and response.message['results'][0]['id'] == '201bc19a-d635-4c10-88be-6c3d310d6afd'

    def test_getting_image_version_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_image_version('40440e67-8644-4949-ba2f-b36c66f9d40b')
        assert not response.ok

    def test_getting_image_version_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_image_version('40440e67-8644-4949-ba2f-b36c66f9d40b')
        assert response.ok
        assert response.message['id'] == '40440e67-8644-4949-ba2f-b36c66f9d40b' and \
            response.message['change_log'] == 'v1.7 - patched up to 9-14-17' and \
            len(response.message['machines']) == 2
