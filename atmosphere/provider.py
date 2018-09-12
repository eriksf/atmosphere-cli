import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from atmosphere.api import AtmosphereAPI
from atmosphere.utils import ts_to_isodate


class ProviderList(Lister):
    """
    List cloud providers managed by Atmosphere.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        column_headers = ('id', 'uuid', 'name', 'type', 'virtualization', 'public', 'active', 'start_date')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_providers()
        providers = []
        if data.ok:
            for provider in data.message['results']:
                start_date = ts_to_isodate(provider['start_date'])
                providers.append((
                    provider['id'],
                    provider['uuid'],
                    provider['name'],
                    provider['type']['name'],
                    provider['virtualization']['name'],
                    provider['public'],
                    provider['active'],
                    start_date if start_date else provider['start_date']
                ))

        return (column_headers, tuple(providers))


class ProviderShow(ShowOne):
    """
    Show details for a cloud provider.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ProviderShow, self).get_parser(prog_name)
        parser.add_argument('id', help='the provider uuid')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('id',
                          'uuid',
                          'name',
                          'description',
                          'type',
                          'virtualization',
                          'sizes',
                          'auto_imaging',
                          'public',
                          'is_admin',
                          'active',
                          'start_date',
                          'end_date')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_provider(parsed_args.id)
        provider = ()
        if data.ok:
            message = data.message
            start_date = ts_to_isodate(message['start_date'])
            end_date = ''
            if message['end_date']:
                end_date = ts_to_isodate(message['end_date'])
            provider = (
                message['id'],
                message['uuid'],
                message['name'],
                message['description'],
                message['type']['name'],
                message['virtualization']['name'],
                ', '.join([value['name'] for value in message['sizes']]),
                message['auto_imaging'],
                message['public'],
                message['is_admin'],
                message['active'],
                start_date,
                end_date
            )

        return (column_headers, provider)
