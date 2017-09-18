import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from atmosphere.api import AtmosphereAPI


class IdentityList(Lister):
    """
    List user identities managed by Atmosphere.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        column_headers = ('id', 'name', 'provider', 'usage', 'quota_cpu', 'quota_memory', 'quota_storage')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_identities()
        identities = []
        for identity in data['results']:
            identities.append((
                identity['id'],
                identity['user']['username'],
                identity['provider']['name'],
                identity['usage'],
                identity['quota']['cpu'],
                identity['quota']['memory'],
                identity['quota']['storage']
            ))

        return (column_headers, tuple(identities))


class IdentityShow(ShowOne):
    """
    Show details for a user identity.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(IdentityShow, self).get_parser(prog_name)
        parser.add_argument('id', help='the identity id')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('id',
                          'uuid',
                          'username',
                          'user_id',
                          'user_uuid',
                          'key',
                          'is_leader',
                          'provider',
                          'provider_id',
                          'provider_uuid',
                          'usage',
                          'quota_cpu',
                          'quota_memory',
                          'quota_storage',
                          'quota_floating_ip_count',
                          'quota_instance_count',
                          'quota_port_count',
                          'quota_snapshot_count',
                          'quota_storage_count')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_identity(parsed_args.id)
        identity = ()
        if data:
            identity = (
                data['id'],
                data['uuid'],
                data['user']['username'],
                data['user']['id'],
                data['user']['uuid'],
                data['key'],
                data['is_leader'],
                data['provider']['name'],
                data['provider']['id'],
                data['provider']['uuid'],
                data['usage'],
                data['quota']['cpu'],
                data['quota']['memory'],
                data['quota']['storage'],
                data['quota']['floating_ip_count'],
                data['quota']['instance_count'],
                data['quota']['port_count'],
                data['quota']['snapshot_count'],
                data['quota']['storage_count']
            )

        return (column_headers, identity)
