import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from atmosphere.api import AtmosphereAPI
from atmosphere.utils import ts_to_isodate


class VolumeList(Lister):
    """
    List volumes for a user.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        column_headers = ('id', 'name', 'project', 'provider', 'size', 'user', 'start_date')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_volumes()
        volumes = []
        for volume in data['results']:
            start_date = ts_to_isodate(volume['start_date'])
            volumes.append((
                volume['id'],
                volume['name'],
                volume['project']['name'],
                volume['provider']['name'],
                volume['size'],
                volume['user']['username'],
                start_date
            ))

        return (column_headers, tuple(volumes))


class VolumeShow(ShowOne):
    """
    Show details for a volume.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(VolumeShow, self).get_parser(prog_name)
        parser.add_argument('id', help='the volume id')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('id',
                          'uuid',
                          'name',
                          'description',
                          'project',
                          'provider',
                          'identity',
                          'size',
                          'user',
                          'start_date',
                          'end_date')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_volume(parsed_args.id)
        volume = ()
        if data:
            volume = (
                data['id'],
                data['uuid'],
                data['name'],
                data['description'],
                data['project']['name'],
                data['provider']['name'],
                data['identity']['key'],
                data['size'],
                data['user']['username'],
                data['start_date'],
                data['end_date']
            )

        return (column_headers, volume)
