import logging
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from six.moves.urllib.parse import urlparse

from .constants import ApiResponse


class Request(object):
    """Class to handle an API request"""

    def __init__(self, token, base_url, timeout, verify):
        self.token = token
        self.base_url = base_url
        self.timeout = timeout
        self.verify = verify
        self.__authorization_header = 'TOKEN {}'.format(self.token)
        url_obj = urlparse(base_url)
        self.__hostname = url_obj.hostname
        self.__port = url_obj.port
        self.__scheme = url_obj.scheme
        self.__prefix = url_obj.geturl()

        if not self.verify:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def __makeFullUrl(self, url):
        if url.startswith('/'):
            url = self.__prefix + url
        else:
            url_obj = urlparse(url)
            assert url_obj.scheme == self.__scheme
            assert url_obj.hostname == self.__hostname
            assert url_obj.path.startswith(self.__prefix)
            assert url_obj.port == self.__port
            url = url_obj.geturl()
        return url

    def __log(self, verb, url, request_headers, input, response):
        logger = logging.getLogger(__name__)
        if logger.isEnabledFor(logging.DEBUG):
            if request_headers and "Authorization" in request_headers:
                if request_headers['Authorization'].startswith('TOKEN'):
                    request_headers['Authorization'] = 'TOKEN (token removed)'
            if response is not None:
                logger.debug('{} {} Headers:{} Input:{} ===> {} Headers:{} Response:{}'.format(
                    verb,
                    url,
                    str(request_headers),
                    input,
                    response.status_code,
                    str(response.headers),
                    response.content))
            else:
                logger.debug('{} {} Headers:{} Input:{} ===> None'.format(verb, url, str(request_headers), input))

    def __log_error(self, message):
        logger = logging.getLogger(__name__)
        if logger.isEnabledFor(logging.ERROR):
            logger.error('ERROR: {}'.format(message))

    def __log_message(self, message):
        logger = logging.getLogger(__name__)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('{}'.format(message))

    def getJson(self, verb, url, params=None, headers=None, data=None):
        method = getattr(requests, verb.lower())

        # add the authorization header
        if not headers:
            headers = {'Authorization': self.__authorization_header}
        else:
            headers['Authorization'] = self.__authorization_header

        # set the format of the response to JSON with Accept header
        headers['Accept'] = 'application/json; indent=4, application/json'

        response = ApiResponse(ok=False, message='')
        try:
            r = method(self.__makeFullUrl(url), params=params, headers=headers, data=data, timeout=self.timeout, verify=self.verify)
            self.__log(verb, url, headers, data, r)
            # consider any status besides 2xx an error
            if r.status_code // 100 == 2:
                # self.__log_message('Response text: {}'.format(r.text))
                if r.text:
                    try:
                        response = ApiResponse(ok=True, message=r.json())
                    except ValueError as ve:
                        # empty or not valid json returned
                        self.__log_error(ve)
                else:
                    response = ApiResponse(ok=True, message='')
            else:
                if r.text:
                    try:
                        failure_response = r.json()
                        self.__log_error(failure_response)
                        response = ApiResponse(ok=False, message=failure_response)
                    except ValueError as ve:
                        self.__log_error(ve)
        except requests.exceptions.RequestException as re:
            self.__log_error(re)
        except Exception as e:
            self.__log_error(e)
        return response
