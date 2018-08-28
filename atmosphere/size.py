import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from atmosphere.api import AtmosphereAPI
from atmosphere.utils import ts_to_isodate


class SizeList(Lister):
    """
    List sizes (instance configurations) for cloud provider.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SizeList, self).get_parser(prog_name)
        parser.add_argument(
            '-p',
            '--provider-id',
            metavar='<provider-id>',
            dest='provider_id',
            help='Filter sizes by the cloud provider id.'
        )
        return parser

    def take_action(self, parsed_args):
        column_headers = ('uuid', 'name', 'alias', 'provider', 'cpu', 'memory', 'disk', 'active', 'start_date')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_sizes(provider_id=parsed_args.provider_id)
        sizes = []
        if data.ok:
            for size in data.message['results']:
                start_date = ts_to_isodate(size['start_date'])
                sizes.append((
                    size['uuid'],
                    size['name'],
                    size['alias'],
                    size['provider']['name'],
                    size['cpu'],
                    size['mem'],
                    size['disk'],
                    size['active'],
                    start_date if start_date else size['start_date']
                ))

        return (column_headers, tuple(sizes))


class SizeShow(ShowOne):
    """
    Show details for a size (instance configuration).
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SizeShow, self).get_parser(prog_name)
        parser.add_argument('id', help='the size uuid')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('id',
                          'uuid',
                          'name',
                          'alias',
                          'provider_id',
                          'provider_name',
                          'provider_uuid',
                          'cpu',
                          'memory',
                          'disk',
                          'active',
                          'root',
                          'start_date',
                          'end_date')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_size(parsed_args.id)
        size = ()
        if data.ok:
            message = data.message
            start_date = ts_to_isodate(message['start_date'])
            end_date = ''
            if message['end_date']:
                end_date = ts_to_isodate(message['end_date'])
            size = (
                message['id'],
                message['uuid'],
                message['name'],
                message['alias'],
                message['provider']['id'],
                message['provider']['name'],
                message['provider']['uuid'],
                message['cpu'],
                message['mem'],
                message['disk'],
                message['active'],
                message['root'],
                start_date,
                end_date
            )

        return (column_headers, size)
