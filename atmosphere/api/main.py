from .request import Request
from .constants import ATMO_BASE_URL, ATMO_API_SERVER_TIMEOUT, ATMO_API_SERVER_VERIFY_CERT


class AtmosphereAPI(object):
    """Main class for accessing the Atmosphere v2 API."""

    def __init__(self, token, base_url=ATMO_BASE_URL, timeout=ATMO_API_SERVER_TIMEOUT, verify=ATMO_API_SERVER_VERIFY_CERT):
        """
        :param token: string
        :param base_url: string
        :param timeout: integer
        :param verify: boolean
        """

        self.__request = Request(token, base_url, timeout, verify)

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

    def get_version(self):
        data = self.__request.getJson('GET', '/version/')
        return data

    def get_identities(self):
        data = self.__request.getJson('GET', '/identities/')
        return data

    def get_identity(self, id):
        data = self.__request.getJson('GET', '/identities/{}'.format(id))
        return data
