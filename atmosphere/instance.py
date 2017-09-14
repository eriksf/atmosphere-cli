import json
import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from atmosphere.api import AtmosphereAPI
from atmosphere.utils import ts_to_isodate


class InstanceCreate(ShowOne):
    """
    Create an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceCreate, self).get_parser(prog_name)
        parser.add_argument('name', help='the instance name')
        parser.add_argument(
            '--identity',
            metavar='<identity>',
            required=True,
            help='Identity UUID'
        )
        parser.add_argument(
            '--size-alias',
            metavar='<size_alias>',
            required=True,
            help='Alias of size/flavor'
        )
        parser.add_argument(
            '--source-alias',
            metavar='<source_alias>',
            required=True,
            help='Alias/identifier of machine or volume'
        )
        parser.add_argument(
            '--project',
            metavar='<project>',
            required=True,
            help='Project UUID'
        )
        parser.add_argument(
            '--allocation-source-id',
            metavar='<allocation_source_id>',
            required=True,
            help='Allocation source UUID'
        )
        parser.add_argument(
            '--no-deploy',
            action='store_false',
            dest='deploy',
            help="Don't run ansible deployments on instance"
        )
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        payload = {
            "name": parsed_args.name,
            "identity": parsed_args.identity,
            "size_alias": parsed_args.size_alias,
            "source_alias": parsed_args.source_alias,
            "project": parsed_args.project,
            "allocation_source_id": parsed_args.allocation_source_id,
            "deploy": parsed_args.deploy,
            "scripts": [],
            "extra": {}
        }
        self.log.debug('INPUT: {}'.format(json.dumps(payload)))
        data = api.create_instance(json.dumps(payload))
        instance = ()
        column_headers = ('id',
                          'uuid',
                          'name',
                          'username',
                          'allocation_source',
                          'image_id',
                          'image_version',
                          'launched',
                          'image_size',
                          'provider')
        if data:
            launched = ts_to_isodate(data['start_date'])
            instance = (
                data['id'],
                data['uuid'],
                data['name'],
                data['user']['username'],
                data['allocation_source']['name'],
                data['image']['id'],
                data['version']['name'],
                launched,
                data['size']['name'],
                data['provider']['name']
            )
        else:
            self.app.stdout.write('Error, instance not created! Make sure to supply name, identity, project, size, source, and allocation_source.')

        return (column_headers, instance)


class InstanceList(Lister):
    """
    List instances for user.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        column_headers = ('id', 'name', 'status', 'activity', 'ip_address', 'size', 'provider', 'launched')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_instances()
        instances = []
        for instance in data['results']:
            launched = ts_to_isodate(instance['start_date'])
            instances.append((
                instance['id'],
                instance['name'],
                instance['status'],
                instance['activity'],
                instance['ip_address'],
                instance['size']['name'],
                instance['provider']['name'],
                launched
            ))

        return (column_headers, tuple(instances))


class InstanceShow(ShowOne):
    """
    Show details for an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceShow, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance id')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('id',
                          'uuid',
                          'name',
                          'username',
                          'allocation_source',
                          'compute_allowed',
                          'compute_used',
                          'user_burn_rate',
                          'image_id',
                          'image_version',
                          'image_usage',
                          'launched',
                          'image_size',
                          'image_cpu',
                          'image_mem',
                          'image_disk',
                          'status',
                          'activity',
                          'ip_address',
                          'provider',
                          'web_desktop',
                          'shell',
                          'vnc')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_instance(parsed_args.id)
        instance = ()
        if data:
            launched = ts_to_isodate(data['start_date'])
            instance = (
                data['id'],
                data['uuid'],
                data['name'],
                data['user']['username'],
                data['allocation_source']['name'],
                data['allocation_source']['compute_allowed'],
                data['allocation_source']['compute_used'],
                data['allocation_source']['user_burn_rate'],
                data['image']['id'],
                data['version']['name'],
                data['usage'],
                launched,
                data['size']['name'],
                data['size']['cpu'],
                data['size']['mem'],
                data['size']['disk'],
                data['status'],
                data['activity'],
                data['ip_address'],
                data['provider']['name'],
                data['web_desktop'],
                data['shell'],
                data['vnc']
            )

        return (column_headers, instance)


class InstanceActions(Lister):
    """
    Show available actions for an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceActions, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance id')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('action', 'description')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_instance_actions(parsed_args.id)
        actions = []
        for action in data:
            actions.append((
                action['name'],
                action['description'],
            ))

        return (column_headers, tuple(actions))
