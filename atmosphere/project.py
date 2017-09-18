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
            help='Project description'
        )
        return parser

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        payload = {
            "name": parsed_args.name,
            "description": parsed_args.description
        }
        self.log.debug('INPUT: {}'.format(json.dumps(payload)))
        data = api.create_project(json.dumps(payload))
        project = ()
        column_headers = ('id', 'uuid', 'name', 'description', 'owner', 'start_date')
        if data:
            start_date = ts_to_isodate(data['start_date'], include_time=True)
            project = (
                data['id'],
                data['uuid'],
                data['name'],
                data['description'],
                data['owner']['username'],
                start_date
            )
        else:
            self.app.stdout.write('Error, project not created! Make sure to supply a name and description.')

        return (column_headers, project)


class ProjectList(Lister):
    """
    List projects for a user.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        column_headers = ('id', 'name', 'description', 'owner', 'created_by', 'start_date', 'images', 'instances', 'volumes', 'links')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_projects()
        projects = []
        for project in data['results']:
            start_date = ts_to_isodate(project['start_date'])
            projects.append((
                project['id'],
                project['name'],
                project['description'],
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
        parser.add_argument('id', help='the project id')
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
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_project(parsed_args.id)
        project = ()
        if data:
            start_date = ts_to_isodate(data['start_date'])
            end_date = ''
            if data['end_date']:
                end_date = ts_to_isodate(data['end_date'])
            project = (
                data['id'],
                data['uuid'],
                data['name'],
                data['description'],
                data['owner']['name'],
                data['created_by']['username'],
                start_date,
                end_date,
                ', '.join([value['username'] for value in data['leaders']]),
                ', '.join([value['username'] for value in data['users']]),
                len(data['images']),
                len(data['instances']),
                len(data['volumes']),
                len(data['links'])
            )

        return (column_headers, project)
