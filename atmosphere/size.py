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
        column_headers = ('Id', 'Name', 'Provider', 'CPU', 'Memory', 'Disk', 'Active?', 'Start Date')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_sizes(provider_id=parsed_args.provider_id)
        sizes = []
        for size in data['results']:
            start_date = ts_to_isodate(size['start_date'])
            sizes.append((
                size['id'],
                size['name'],
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
        parser.add_argument('id', help='the size id')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('Id', 'Name', 'Alias', 'Provider', 'CPU', 'Memory', 'Disk', 'Active?', 'Root', 'Start Date')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_size(parsed_args.id)
        size = ()
        if data:
            start_date = ts_to_isodate(data['start_date'])
            size = (
                data['id'],
                data['name'],
                data['alias'],
                data['provider']['name'],
                data['cpu'],
                data['mem'],
                data['disk'],
                data['active'],
                data['root'],
                start_date if start_date else data['start_date']
            )

        return (column_headers, size)