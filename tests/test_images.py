import re
from mock_server import get_free_port, start_mock_server
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
        assert not response

    def test_getting_images_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_images()
        assert response['count'] == 1 and response['results'][0]['name'] == 'name'

    def test_getting_images_when_response_is_ok_and_filtering_on_tag(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_images(tag_name='docker')
        results = response['results']
        fcount = 0
        for r in results:
            if is_term_in_image_result(r, 'docker'):
                fcount += 1
        assert response['count'] == 11 and fcount == 11

    def test_getting_images_when_response_is_ok_and_filtering_on_creator(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_images(created_by='jfischer')
        results = response['results']
        fcount = 0
        for r in results:
            if is_term_in_image_result(r, 'jfischer'):
                fcount += 1
        assert response['count'] == 9 and fcount == 9

    def test_searching_images_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.search_images('galaxy')
        results = response['results']
        fcount = 0
        for r in results:
            if is_term_in_image_result(r, 'galaxy'):
                fcount += 1
        assert response['count'] == 3 and fcount == 3

    def test_getting_image_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_image(1)
        assert not response

    def test_getting_image_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_image(1)
        assert response['id'] == 1 and response['name'] == 'name'
