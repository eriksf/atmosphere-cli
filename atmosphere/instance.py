import json
import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from cliff.command import Command
from atmosphere.api import AtmosphereAPI
from atmosphere.utils import ts_to_isodate, ts_to_date


class InstanceDelete(Command):
    """
    Delete an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceDelete, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance uuid')
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            help="Don't ask for confirmation before deleting instance"
        )
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        if parsed_args.delete:
            data = api.delete_instance(parsed_args.id)
            if data.ok and data.message and data.message != '':
                self.app.stdout.write('Instance deleted: {}\n'.format(data.message))
            else:
                self.app.stdout.write('Instance deleted\n')


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
            help='Identity UUID [required]'
        )
        parser.add_argument(
            '--size-alias',
            metavar='<size_alias>',
            required=True,
            help='Alias of size/flavor [required]'
        )
        source_group = parser.add_mutually_exclusive_group(required=True)
        source_group.add_argument(
            '--source-alias',
            metavar='<source_alias>',
            help='Alias/identifier UUID of machine or volume [required]'
        )
        source_group.add_argument(
            '--image',
            metavar='<image>',
            help='Image UUID (Uses the latest image version) [required]'
        )
        parser.add_argument(
            '--project',
            metavar='<project>',
            required=True,
            help='Project UUID [required]'
        )
        parser.add_argument(
            '--allocation-source-id',
            metavar='<allocation_source_id>',
            required=True,
            help='Allocation source UUID [required]'
        )
        parser.add_argument(
            '--no-deploy',
            action='store_false',
            dest='deploy',
            help="Don't run ansible deployments on instance"
        )
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        payload = {
            "name": parsed_args.name,
            "identity": parsed_args.identity,
            "size_alias": parsed_args.size_alias,
            "project": parsed_args.project,
            "allocation_source_id": parsed_args.allocation_source_id,
            "deploy": parsed_args.deploy,
            "scripts": [],
            "extra": {}
        }

        if parsed_args.image:
            # get the provider from the identity
            payload['source_alias'] = None
            id_data = api.get_identity(parsed_args.identity)
            if id_data.ok:
                provider_id = id_data.message['provider']['id']
                self.log.debug('Found provider id {} for identity uuid {}'.format(provider_id, parsed_args.identity))

                # get the provider machine from the latest image version
                v_data = api.get_image_versions(parsed_args.image)
                if v_data.ok:
                    # get latest image version
                    latest_version = v_data.message['results'][-1]
                    machines = latest_version['machines']
                    machine_id = next((m['uuid'] for m in machines if m['provider']['id'] == provider_id), None)
                    self.log.debug('Found machine id {} for latest image version {} and provider id {}'.format(machine_id, latest_version['name'], provider_id))
                    payload['source_alias'] = machine_id
                else:
                    self.app.stdout.write('Error, instance not created. Could not lookup latest image version from image uuid supplied: {}'.format(parsed_args.image))
            else:
                self.app.stdout.write('Error, instance not created. Could not lookup provider from identity uuid supplied: {}'.format(parsed_args.identity))
        else:
            payload['source_alias'] = parsed_args.source_alias

        self.log.debug('INPUT: {}'.format(json.dumps(payload)))
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

        if payload['source_alias']:
            data = api.create_instance(json.dumps(payload))

            if data.ok:
                message = data.message
                launched = ts_to_isodate(message['start_date'])
                instance = (
                    message['id'],
                    message['uuid'],
                    message['name'],
                    message['user']['username'],
                    message['allocation_source']['name'],
                    message['image']['id'],
                    message['version']['name'],
                    launched,
                    message['size']['name'],
                    message['provider']['name']
                )
            else:
                self.app.stdout.write('Error, instance not created! Make sure to supply name, identity, project, size, source (or image), and allocation_source.')

        return (column_headers, instance)


class InstanceList(Lister):
    """
    List instances for user.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        column_headers = ('uuid', 'name', 'status', 'activity', 'ip_address', 'size', 'provider', 'project', 'launched')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_instances()
        instances = []
        if data.ok:
            for instance in data.message['results']:
                launched = ts_to_isodate(instance['start_date'])
                instances.append((
                    instance['uuid'],
                    instance['name'],
                    instance['status'],
                    instance['activity'],
                    instance['ip_address'],
                    instance['size']['name'],
                    instance['provider']['name'],
                    instance['project']['name'],
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
        parser.add_argument('id', help='the instance uuid')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('id',
                          'uuid',
                          'name',
                          'username',
                          'identity',
                          'project',
                          'allocation_source',
                          'compute_allowed',
                          'compute_used',
                          'global_burn_rate',
                          'user_compute_used',
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
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_instance(parsed_args.id)
        instance = ()
        if data.ok:
            message = data.message
            launched = ts_to_isodate(message['start_date'])
            instance = (
                message['id'],
                message['uuid'],
                message['name'],
                message['user']['username'],
                message['identity']['key'],
                message['project']['name'],
                message['allocation_source']['name'],
                message['allocation_source']['compute_allowed'],
                message['allocation_source']['compute_used'],
                message['allocation_source']['global_burn_rate'],
                message['allocation_source']['user_compute_used'],
                message['allocation_source']['user_burn_rate'],
                message['image']['id'],
                message['version']['name'],
                message['usage'],
                launched,
                message['size']['name'],
                message['size']['cpu'],
                message['size']['mem'],
                message['size']['disk'],
                message['status'],
                message['activity'],
                message['ip_address'],
                message['provider']['name'],
                message['web_desktop'],
                message['shell'],
                message['vnc']
            )

        return (column_headers, instance)


class InstanceActions(Lister):
    """
    Show available actions for an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceActions, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance uuid')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('action', 'description')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_instance_actions(parsed_args.id)
        actions = []
        if data.ok:
            for action in data.message:
                actions.append((
                    action['name'],
                    action['description'],
                ))

        return (column_headers, tuple(actions))


class InstanceSuspend(Command):
    """
    Suspend an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceSuspend, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance uuid')
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.do_instance_action('suspend', parsed_args.id)
        if data.ok and data.message['result'] == 'success':
            self.app.stdout.write('{}\n'.format(data.message['message']))
        else:
            self.app.stdout.write('Error: {}\n'.format(data.message))


class InstanceResume(Command):
    """
    Resume an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceResume, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance uuid')
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.do_instance_action('resume', parsed_args.id)
        if data.ok and data.message['result'] == 'success':
            self.app.stdout.write('{}\n'.format(data.message['message']))
        else:
            self.app.stdout.write('Error: {}\n'.format(data.message))


class InstanceReboot(Command):
    """
    Reboot an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceReboot, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance uuid')
        parser.add_argument(
            '--hard',
            action='store_true',
            dest='hard_reboot',
            help="Perform a hard reboot on the instance"
        )
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        options = None
        if parsed_args.hard_reboot:
            options = {'reboot_type': 'HARD'}
        data = api.do_instance_action('reboot', parsed_args.id, options=options)
        if data.ok and data.message['result'] == 'success':
            self.app.stdout.write('{}\n'.format(data.message['message']))
        else:
            self.app.stdout.write('Error: {}\n'.format(data.message))


class InstanceStop(Command):
    """
    Stop an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceStop, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance uuid')
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.do_instance_action('stop', parsed_args.id)
        if data.ok and data.message['result'] == 'success':
            self.app.stdout.write('{}\n'.format(data.message['message']))
        else:
            self.app.stdout.write('Error: {}\n'.format(data.message))


class InstanceStart(Command):
    """
    Start an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceStart, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance uuid')
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.do_instance_action('start', parsed_args.id)
        if data.ok and data.message['result'] == 'success':
            self.app.stdout.write('{}\n'.format(data.message['message']))
        else:
            self.app.stdout.write('Error: {}\n'.format(data.message))


class InstanceRedeploy(Command):
    """
    Redeploy to an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceRedeploy, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance uuid')
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.do_instance_action('redeploy', parsed_args.id)
        if data.ok and data.message['result'] == 'success':
            self.app.stdout.write('{}\n'.format(data.message['message']))
        else:
            self.app.stdout.write('Error: {}\n'.format(data.message))


class InstanceShelve(Command):
    """
    Shelve an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceShelve, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance uuid')
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.do_instance_action('shelve', parsed_args.id)
        if data.ok and data.message['result'] == 'success':
            self.app.stdout.write('{}\n'.format(data.message['message']))
        else:
            self.app.stdout.write('Error: {}\n'.format(data.message))


class InstanceUnshelve(Command):
    """
    Unshelve an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceUnshelve, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance uuid')
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.do_instance_action('unshelve', parsed_args.id)
        if data.ok and data.message['result'] == 'success':
            self.app.stdout.write('{}\n'.format(data.message['message']))
        else:
            self.app.stdout.write('Error: {}\n'.format(data.message))


class InstanceAttach(Command):
    """
    Attach a volume to an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceAttach, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance uuid')
        parser.add_argument(
            '--volume-id',
            metavar='<volume_id>',
            required=True,
            help='Volume UUID [required]'
        )
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        options = {'volume_id': parsed_args.volume_id}
        data = api.do_instance_volume_action('attach_volume', parsed_args.id, options=options)
        if data.ok and data.message['result'] == 'success':
            self.app.stdout.write('{}\n'.format(data.message['message']))
        else:
            self.app.stdout.write('Error: {}\n'.format(data.message))


class InstanceDetach(Command):
    """
    Detach a volume from an instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceDetach, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance uuid')
        parser.add_argument(
            '--volume-id',
            metavar='<volume_id>',
            required=True,
            help='Volume UUID [required]'
        )
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        options = {'volume_id': parsed_args.volume_id}
        data = api.do_instance_volume_action('detach_volume', parsed_args.id, options=options)
        if data.ok and data.message['result'] == 'success':
            self.app.stdout.write('{}\n'.format(data.message['message']))
        else:
            self.app.stdout.write('Error: {}\n'.format(data.message))


class InstanceHistory(Lister):
    """
    List history for instance.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstanceHistory, self).get_parser(prog_name)
        parser.add_argument('id', help='the instance uuid')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('uuid', 'name', 'size', 'provider', 'status', 'start_date', 'end_date')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_instance_history(parsed_args.id)
        history = []
        if data.ok:
            for status in data.message['results']:
                start_date = ts_to_date(status['start_date'])
                end_date = ''
                if status['end_date']:
                    end_date = ts_to_date(status['end_date'])
                history.append((
                    status['instance']['uuid'],
                    status['instance']['name'],
                    status['size']['name'],
                    status['provider']['name'],
                    status['status'],
                    start_date,
                    end_date,
                ))

        return (column_headers, tuple(history))
