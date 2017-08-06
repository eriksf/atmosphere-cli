import logging
import requests
from urllib.parse import urlparse
# import constants


class Request(object):
    """Class to handle an API request"""

    def __init__(self, login_or_token, password, base_url, timeout):
        if password is not None:
            self.login = login_or_token
        elif login_or_token is not None:
            self.token = login_or_token
        else:
            pass

        self.base_url = base_url
        self.timeout = timeout
        url_obj = urlparse(base_url)
        self.__hostname = url_obj.hostname
        self.__port = url_obj.port
        self.__scheme = url_obj.scheme
        self.__prefix = url_obj.geturl()

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
            if "Authorization" in request_headers:
                if request_headers['Authorization'].startswith('Token'):
                    request_headers['Authorization'] = 'Token (token removed)'
                else:
                    request_headers['Authorization'] = '(unknown auth removed)'
            if response:
                logger.debug('{} {} {} {} ==> {} {} {}'.format(verb,
                                                               url,
                                                               str(request_headers),
                                                               input,
                                                               response.status_code,
                                                               str(response.headers),
                                                               response.content))
            else:
                logger.debug('{} {} {} {} ==> None'.format(verb, url, str(request_headers), input))

    def getJson(self, verb, url, params=None, headers=None, data=None):
        method = getattr(requests, verb.lower())
        data = None
        try:
            r = method(self.__makeFullUrl(url), params=params, headers=headers, data=data, timeout=self.timeout)
            self.__log(verb, url, headers, data, r)
            data = r.json()
        except requests.exceptions.RequestException:
            pass
        return data
