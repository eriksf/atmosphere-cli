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
        column_headers = ('Id', 'Name', 'Provider', 'Allocation', 'Usage Current', 'Usage Remaining', 'Quota CPU', 'Quota Memory', 'Quota Storage')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_identities()
        identities = []
        for identity in data['results']:
            identities.append((
                identity['id'],
                identity['user']['username'],
                identity['provider']['name'],
                identity['allocation']['threshold'],
                identity['usage']['current'],
                identity['usage']['remaining'],
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
        column_headers = ('Id',
                          'UUID',
                          'Username',
                          'User Id',
                          'User UUID',
                          'Provider',
                          'Provider Id',
                          'Provider UUID',
                          'Allocation Id',
                          'Allocation UUID',
                          'Allocation Threshold',
                          'Allocation Delta',
                          'Usage Current',
                          'Usage Remaining',
                          'Usage Threshold',
                          'Quota CPU',
                          'Quota Memory',
                          'Quota Storage',
                          'Quota Floating IP Count',
                          'Quota Instance Count',
                          'Quota Port Count',
                          'Quota Snapshot Count',
                          'Quota Storage Count')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_identity(parsed_args.id)
        identity = ()
        if data:
            identity = (
                data['id'],
                data['uuid'],
                data['user']['id'],
                data['user']['username'],
                data['user']['uuid'],
                data['provider']['id'],
                data['provider']['name'],
                data['provider']['uuid'],
                data['allocation']['id'],
                data['allocation']['uuid'],
                data['allocation']['threshold'],
                data['allocation']['delta'],
                data['usage']['current'],
                data['usage']['remaining'],
                data['usage']['threshold'],
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
