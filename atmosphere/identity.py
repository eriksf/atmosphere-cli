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
        column_headers = ('uuid', 'name', 'provider', 'quota_cpu', 'quota_memory', 'quota_storage')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_identities()
        identities = []
        if data.ok:
            for identity in data.message['results']:
                identities.append((
                    identity['uuid'],
                    identity['user']['username'],
                    identity['provider']['name'],
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
        parser.add_argument('id', help='the identity uuid')
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
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_identity(parsed_args.id)
        identity = ()
        if data.ok:
            message = data.message
            identity = (
                message['id'],
                message['uuid'],
                message['user']['username'],
                message['user']['id'],
                message['user']['uuid'],
                message['key'],
                message['is_leader'],
                message['provider']['name'],
                message['provider']['id'],
                message['provider']['uuid'],
                message['usage'],
                message['quota']['cpu'],
                message['quota']['memory'],
                message['quota']['storage'],
                message['quota']['floating_ip_count'],
                message['quota']['instance_count'],
                message['quota']['port_count'],
                message['quota']['snapshot_count'],
                message['quota']['storage_count']
            )

        return (column_headers, identity)
