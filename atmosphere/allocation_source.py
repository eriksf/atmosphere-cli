import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from atmosphere.api import AtmosphereAPI
from atmosphere.utils import ts_to_isodate


class AllocationSourceList(Lister):
    """
    List allocation sources for a user.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        column_headers = ('uuid', 'name', 'compute_allowed', 'compute_used', 'global_burn_rate', 'start_date')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_allocation_sources()
        allocation_sources = []
        if data.ok:
            for source in data.message['results']:
                start_date = ts_to_isodate(source['start_date'])
                allocation_sources.append((
                    source['uuid'],
                    source['name'],
                    source['compute_allowed'],
                    source['compute_used'],
                    source['global_burn_rate'],
                    start_date
                ))

        return (column_headers, tuple(allocation_sources))


class AllocationSourceShow(ShowOne):
    """
    Show details for an allocation source.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(AllocationSourceShow, self).get_parser(prog_name)
        parser.add_argument('id', help='the allocation source uuid')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('id',
                          'uuid',
                          'name',
                          'renewal_strategy',
                          'compute_allowed',
                          'compute_used',
                          'global_burn_rate',
                          'user_compute_used',
                          'user_burn_rate',
                          'start_date',
                          'end_date')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_allocation_source(parsed_args.id)
        allocation_source = ()
        if data.ok:
            message = data.message
            start_date = ts_to_isodate(message['start_date'])
            end_date = ''
            if message['end_date']:
                end_date = ts_to_isodate(message['end_date'])
            allocation_source = (
                message['id'],
                message['uuid'],
                message['name'],
                message['renewal_strategy'],
                message['compute_allowed'],
                message['compute_used'],
                message['global_burn_rate'],
                message['user_compute_used'],
                message['user_burn_rate'],
                start_date,
                end_date
            )

        return (column_headers, allocation_source)
