from .request import Request
from .constants import ATMO_BASE_URL, DEFAULT_TIMEOUT


class AtmosphereAPI(object):
    """Main class for accessing the Atmosphere v2 API."""

    def __init__(self, token, base_url=ATMO_BASE_URL, timeout=DEFAULT_TIMEOUT):
        """
        :param token: string
        :param base_url: string
        :param timeout: integer
        """

        self.__request = Request(token, base_url, timeout)

    def get_images(self):
        data = self.__request.getJson('GET', '/images/')
        return data

    def get_image(self, id):
        data = self.__request.getJson('GET', '/images/{}'.format(id))
        return data

    def get_providers(self):
        data = self.__request.getJson('GET', '/providers/')
        return data

    def get_provider(self, id):
        data = self.__request.getJson('GET', '/providers/{}'.format(id))
        return data
