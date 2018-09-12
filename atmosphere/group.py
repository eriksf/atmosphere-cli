import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from atmosphere.api import AtmosphereAPI


class GroupList(Lister):
    """
    List groups for a user.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        column_headers = ('uuid', 'name')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_groups()
        groups = []
        if data.ok:
            for group in data.message['results']:
                groups.append((
                    group['uuid'],
                    group['name']
                ))

        return (column_headers, tuple(groups))


class GroupShow(ShowOne):
    """
    Show details for a group.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GroupShow, self).get_parser(prog_name)
        parser.add_argument('id', help='the group uuid')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('uuid',
                          'name',
                          'users',
                          'leaders')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_group(parsed_args.id)
        group = ()
        if data.ok:
            message = data.message
            group = (
                message['uuid'],
                message['name'],
                '\n'.join([value['username'] for value in message['users']]),
                '\n'.join([value['username'] for value in message['leaders']])
            )

        return (column_headers, group)
