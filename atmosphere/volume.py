import json
import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from cliff.command import Command
from atmosphere.api import AtmosphereAPI
from atmosphere.utils import ts_to_isodate


class VolumeDelete(Command):
    """
    Delete a volume.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(VolumeDelete, self).get_parser(prog_name)
        parser.add_argument('id', help='the volume id')
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        if parsed_args.delete:
            data = api.delete_volume(parsed_args.id)
            if data.ok:
                self.app.stdout.write('Volume deleted: {}\n'.format(data.message))
            else:
                self.app.stdout.write('Volume deleted\n')


class VolumeCreate(ShowOne):
    """
    Create a volume.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(VolumeCreate, self).get_parser(prog_name)
        parser.add_argument('name', help='the volume name')
        parser.add_argument(
            '--identity',
            metavar='<identity>',
            required=True,
            help='Identity UUID'
        )
        parser.add_argument(
            '--size',
            metavar='<size>',
            required=True,
            help='Size (in GB)'
        )
        parser.add_argument(
            '--project',
            metavar='<project>',
            required=True,
            help='Project UUID'
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            required=True,
            help='Volume description')
        base_group = parser.add_mutually_exclusive_group()
        base_group.add_argument(
            '--snapshot-id',
            metavar='<snapshot_id>',
            help='Snapshot UUID to use as base for volume')
        base_group.add_argument(
            '--image-id',
            metavar='<image_id>',
            help='Image UUID to use as base for volume')
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        payload = {
            "name": parsed_args.name,
            "identity": parsed_args.identity,
            "size": parsed_args.size,
            "project": parsed_args.project,
            "description": parsed_args.description
        }
        if parsed_args.snapshot_id:
            payload['snapshot_id'] = parsed_args.snapshot_id
        if parsed_args.image_id:
            payload['image_id'] = parsed_args.image_id
        self.log.debug('INPUT: {}'.format(json.dumps(payload)))
        data = api.create_volume(json.dumps(payload))
        volume = ()
        column_headers = ('id', 'uuid', 'name', 'description', 'size', 'project', 'provider', 'user', 'start_date')
        if data.ok:
            message = data.message
            start_date = ts_to_isodate(message['start_date'], include_time=True)
            volume = (
                message['id'],
                message['uuid'],
                message['name'],
                message['description'],
                message['size'],
                message['project']['name'],
                message['provider']['name'],
                message['user']['username'],
                start_date
            )
        else:
            self.app.stdout.write('Error, volume not created! Make sure to supply a name, identity, size, project, and description.')

        return (column_headers, volume)


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
        if data.ok:
            for volume in data.message['results']:
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
        if data.ok:
            message = data.message
            volume = (
                message['id'],
                message['uuid'],
                message['name'],
                message['description'],
                message['project']['name'],
                message['provider']['name'],
                message['identity']['key'],
                message['size'],
                message['user']['username'],
                message['start_date'],
                message['end_date']
            )

        return (column_headers, volume)
