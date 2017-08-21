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
        column_headers = ('Id', 'Name', 'Description', 'Type', 'Virtualization', 'Size(s)', 'Is Public?', 'Is Active?', 'Start Date')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_providers()
        providers = []
        for provider in data['results']:
            start_date = ts_to_isodate(provider['start_date'])
            providers.append((
                provider['id'],
                provider['name'],
                provider['description'],
                provider['type']['name'],
                provider['virtualization']['name'],
                ', '.join([value['name'] for value in provider['sizes']]),
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
        parser.add_argument('id', help='the image id')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('Id',
                          'UUID',
                          'Name',
                          'Description',
                          'Type',
                          'Virtualization',
                          'Size(s)',
                          'Auto Imaging?',
                          'Is Public?',
                          'Is Admin?',
                          'Is Active?',
                          'Start Date',
                          'End Date')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_provider(parsed_args.id)
        provider = ()
        if data:
            start_date = ts_to_isodate(data['start_date'])
            end_date = ''
            if data['end_date']:
                end_date = ts_to_isodate(data['end_date'])
            provider = (
                data['id'],
                data['uuid'],
                data['name'],
                data['description'],
                data['type']['name'],
                data['virtualization']['name'],
                ', '.join([value['name'] for value in data['sizes']]),
                data['auto_imaging'],
                data['public'],
                data['is_admin'],
                data['active'],
                start_date,
                end_date
            )

        return (column_headers, provider)
