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

    def get_instances(self):
        data = self.__request.getJson('GET', '/instances')
        return data

    def get_instance(self, id):
        data = self.__request.getJson('GET', '/instances/{}'.format(id))
        return data

    def create_instance(self, input):
        headers = {'Content-Type': 'application/json'}
        data = self.__request.getJson('POST', '/instances', headers=headers, data=input)
        return data

    def delete_instance(self, id):
        data = self.__request.getJson('DELETE', '/instances/{}'.format(id))
        return data

    def get_instance_actions(self, id):
        udata = self.__request.getJson('GET', '/instances/{}'.format(id))
        data = None
        if udata:
            uuid = udata['uuid']
            data = self.__request.getJson('GET', '/instances/{}/actions'.format(uuid))
        return data

    def get_images(self, tag_name=None, created_by=None, project_id=None):
        if tag_name or created_by or project_id:
            params = {}
            if tag_name:
                params['tag_name'] = tag_name
            if created_by:
                params['created_by'] = created_by
            if project_id:
                params['project_id'] = project_id
            data = self.__request.getJson('GET', '/images', params=params)
        else:
            data = self.__request.getJson('GET', '/images')
        return data

    def get_image(self, id):
        data = self.__request.getJson('GET', '/images/{}'.format(id))
        return data

    def search_images(self, search_term=None):
        params = {'search': search_term}
        data = self.__request.getJson('GET', '/images', params=params)
        return data

    def get_providers(self):
        data = self.__request.getJson('GET', '/providers')
        return data

    def get_provider(self, id):
        data = self.__request.getJson('GET', '/providers/{}'.format(id))
        return data

    def get_version(self):
        data = self.__request.getJson('GET', '/version')
        return data

    def get_identities(self):
        data = self.__request.getJson('GET', '/identities')
        return data

    def get_identity(self, id):
        data = self.__request.getJson('GET', '/identities/{}'.format(id))
        return data

    def get_allocation_sources(self):
        data = self.__request.getJson('GET', '/allocation_sources')
        return data

    def get_allocation_source(self, id):
        data = self.__request.getJson('GET', '/allocation_sources/{}'.format(id))
        return data

    def get_sizes(self, provider_id=None):
        if provider_id:
            params = {'provider__id': provider_id}
            data = self.__request.getJson('GET', '/sizes', params=params)
        else:
            data = self.__request.getJson('GET', '/sizes')
        return data

    def get_size(self, id):
        data = self.__request.getJson('GET', '/sizes/{}'.format(id))
        return data

    def get_projects(self):
        data = self.__request.getJson('GET', '/projects')
        return data

    def get_project(self, id):
        data = self.__request.getJson('GET', '/projects/{}'.format(id))
        return data

    def create_project(self, input):
        headers = {'Content-Type': 'application/json'}
        data = self.__request.getJson('POST', '/projects', headers=headers, data=input)
        return data

    def get_volumes(self):
        data = self.__request.getJson('GET', '/volumes')
        return data

    def get_volume(self, id):
        data = self.__request.getJson('GET', '/volumes/{}'.format(id))
        return data

    def create_volume(self, input):
        headers = {'Content-Type': 'application/json'}
        data = self.__request.getJson('POST', '/volumes', headers=headers, data=input)
        return data
