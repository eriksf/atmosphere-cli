from .request import Request
from .constants import DEFAULT_BASE_URL, DEFAULT_TIMEOUT


class AtmosphereAPI(object):
    """Main class for accessing the Atmosphere v2 API."""

    def __init__(self, login_or_token, password, base_url=DEFAULT_BASE_URL, timeout=DEFAULT_TIMEOUT):
        """
        :param login_or_token: string
        :param password: string
        :param base_url: string
        :param timeout: integer
        """

        self.__request = Request(login_or_token, password, base_url, timeout)

    def get_images(self):
        data = self.__request.getJson('GET', '/images/')
        return data
