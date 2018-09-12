import json
import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from atmosphere.api import AtmosphereAPI
from atmosphere.utils import ts_to_isodate


class ProjectCreate(ShowOne):
    """
    Create a project.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ProjectCreate, self).get_parser(prog_name)
        parser.add_argument('name', help='the project name')
        parser.add_argument(
            '--description',
            metavar='<description>',
            required=True,
            help='Project description [required]'
        )
        parser.add_argument(
            '--owner',
            metavar='<owner>',
            required=True,
            help='Group name [required]'
        )
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        payload = {
            "name": parsed_args.name,
            "description": parsed_args.description,
            "owner": parsed_args.owner
        }
        self.log.debug('INPUT: {}'.format(json.dumps(payload)))
        data = api.create_project(json.dumps(payload))
        project = ()
        column_headers = ('id', 'uuid', 'name', 'description', 'owner', 'start_date')
        if data.ok:
            message = data.message
            project = (
                message['id'],
                message['uuid'],
                message['name'],
                message['description'],
                message['owner']['name'],
                message['start_date']
            )
        else:
            self.app.stdout.write('Error, project not created! Make sure to supply a name, description, and owner (group name).')

        return (column_headers, project)


class ProjectList(Lister):
    """
    List projects for a user.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        column_headers = ('uuid', 'name', 'owner', 'created_by', 'start_date', 'images', 'instances', 'volumes', 'links')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_projects()
        projects = []
        if data.ok:
            for project in data.message['results']:
                start_date = ts_to_isodate(project['start_date'])
                projects.append((
                    project['uuid'],
                    project['name'],
                    project['owner']['name'],
                    project['created_by']['username'],
                    start_date,
                    len(project['images']),
                    len(project['instances']),
                    len(project['volumes']),
                    len(project['links'])
                ))

        return (column_headers, tuple(projects))


class ProjectShow(ShowOne):
    """
    Show details for a project.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ProjectShow, self).get_parser(prog_name)
        parser.add_argument('id', help='the project uuid')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('id',
                          'uuid',
                          'name',
                          'description',
                          'owner',
                          'created_by',
                          'start_date',
                          'end_date',
                          'leaders',
                          'users',
                          'images',
                          'instances',
                          'volumes',
                          'links')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_project(parsed_args.id)
        project = ()
        if data.ok:
            message = data.message
            start_date = ts_to_isodate(message['start_date'])
            end_date = ''
            if message['end_date']:
                end_date = ts_to_isodate(message['end_date'])
            project = (
                message['id'],
                message['uuid'],
                message['name'],
                message['description'],
                message['owner']['name'],
                message['created_by']['username'],
                start_date,
                end_date,
                ', '.join([value['username'] for value in message['leaders']]),
                ', '.join([value['username'] for value in message['users']]),
                len(message['images']),
                len(message['instances']),
                len(message['volumes']),
                len(message['links'])
            )

        return (column_headers, project)
