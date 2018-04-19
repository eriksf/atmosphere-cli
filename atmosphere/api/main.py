import json
import logging
from .request import Request
from .constants import ATMO_BASE_URL, ATMO_API_SERVER_TIMEOUT, ATMO_API_SERVER_VERIFY_CERT, ApiResponse


class ExpiredTokenException(Exception):
    """An exception called when an expired token is detected."""
    pass


class AtmosphereAPI(object):
    """Main class for accessing the Atmosphere v2 API."""

    log = logging.getLogger(__name__)

    def __init__(self, token, base_url=ATMO_BASE_URL, timeout=ATMO_API_SERVER_TIMEOUT, verify=ATMO_API_SERVER_VERIFY_CERT):
        """
        :param token: string
        :param base_url: string
        :param timeout: integer
        :param verify: boolean
        """

        self.__request = Request(token, base_url, timeout, verify)
        self.__username = ''

        # set username
        user_data = self.__request.getJson('GET', '/tokens/{}'.format(token))
        if user_data.ok:
            self.__username = user_data.message['user']['username']
        else:
            # HACK: shouldn't need this if an expired token is properly returning a 403 Forbidden credentials error
            raise ExpiredTokenException('The token in use cannot be found and is most likely expired. Please grab a current token.')

    def get_username(self):
        return self.__username

    def get_instances(self):
        data = self.__request.getJson('GET', '/instances')
        return data

    def get_instance(self, id):
        data = self.__request.getJson('GET', '/instances/{}'.format(id))
        return data

    def get_instance_history(self, id):
        params = {'instance': id}
        data = self.__request.getJson('GET', '/instance_histories', params=params)
        return data

    def create_instance(self, input):
        headers = {'Content-Type': 'application/json'}
        data = self.__request.getJson('POST', '/instances', headers=headers, data=input)
        return data

    def delete_instance(self, id):
        data = self.__request.getJson('DELETE', '/instances/{}'.format(id))
        return data

    def do_instance_action(self, action, id, options=None):
        # check if action is available on instance
        (is_available, available_actions) = self.__is_available_instance_action(action, id)
        if is_available:
            headers = {'Content-Type': 'application/json'}
            payload = {'action': action}
            if options:
                for option, value in options.items():
                    payload[option] = value
            self.log.debug('INPUT: {}'.format(json.dumps(payload)))
            data = self.__request.getJson('POST', '/instances/{}/actions'.format(id), headers=headers, data=json.dumps(payload))
        else:
            available_actions_str = ', '.join(available_actions.keys())
            message = "Can't perform {} on instance. Available actions are {}.".format(action, available_actions_str)
            data = ApiResponse(ok=False, message=message)
        return data

    def do_instance_volume_action(self, action, id, options=None):
        headers = {'Content-Type': 'application/json'}
        payload = {'action': action}
        if options:
            for option, value in options.items():
                payload[option] = value
        self.log.debug('INPUT: {}'.format(json.dumps(payload)))
        data = self.__request.getJson('POST', '/instances/{}/actions'.format(id), headers=headers, data=json.dumps(payload))
        return data

    def get_instance_actions(self, id):
        data = self.__request.getJson('GET', '/instances/{}/actions'.format(id))
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

    def get_image_versions(self, id):
        image_id = self.__get_image_id_from_image_uuid(id)
        params = {'image_id': image_id}
        data = self.__request.getJson('GET', '/image_versions', params=params)
        return data

    def get_image_version(self, id):
        data = self.__request.getJson('GET', '/image_versions/{}'.format(id))
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

    def delete_volume(self, id):
        data = self.__request.getJson('DELETE', '/volumes/{}'.format(id))
        return data

    def __is_available_instance_action(self, action, id):
        # get available actions on instance
        available_actions = {}
        data = self.__request.getJson('GET', '/instances/{}/actions'.format(id))
        if data.ok:
            for available_action in data.message:
                available_actions[available_action['key'].lower()] = available_action['description']
        return (action.lower() in available_actions, available_actions)

    def __get_image_id_from_image_uuid(self, uuid):
        data = self.get_image(uuid)
        if data.ok:
            return data.message['id']
