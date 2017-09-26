import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from atmosphere.api import AtmosphereAPI
from atmosphere.utils import ts_to_isodate


class ImageSearch(Lister):
    """
    Search images for user.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ImageSearch, self).get_parser(prog_name)
        parser.add_argument('search_term', help='the search term')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('id', 'name', 'description', 'created_by', 'versions', 'is_public', 'start_date')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.search_images(parsed_args.search_term)
        images = []
        for image in data['results']:
            start_date = ts_to_isodate(image['start_date'])
            images.append((
                image['id'],
                image['name'],
                image['description'],
                image['created_by']['username'],
                ', '.join([value['name'] for value in image['versions']]),
                image['is_public'],
                start_date if start_date else image['start_date']
            ))

        return (column_headers, tuple(images))


class ImageList(Lister):
    """
    List images for user.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ImageList, self).get_parser(prog_name)
        parser.add_argument(
            '--tag-name',
            metavar='<tag-name>',
            dest='tag_name',
            help='Filter images by the tag name.'
        )
        parser.add_argument(
            '--created-by',
            metavar='<created-by>',
            dest='created_by',
            help='Filter images by the creator name.'
        )
        parser.add_argument(
            '--project-id',
            metavar='<project-id>',
            dest='project_id',
            help='Filter images by the project UUID.'
        )
        return parser

    def take_action(self, parsed_args):
        column_headers = ('id', 'name', 'description', 'created_by', 'versions', 'is_public', 'start_date')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_images(parsed_args.tag_name, parsed_args.created_by, parsed_args.project_id)
        images = []
        for image in data['results']:
            start_date = ts_to_isodate(image['start_date'])
            images.append((
                image['id'],
                image['name'],
                image['description'],
                image['created_by']['username'],
                ', '.join([value['name'] for value in image['versions']]),
                image['is_public'],
                start_date if start_date else image['start_date']
            ))

        return (column_headers, tuple(images))


class ImageShow(ShowOne):
    """
    Show details for an image.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ImageShow, self).get_parser(prog_name)
        parser.add_argument('id', help='the image id')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('id',
                          'uuid',
                          'name',
                          'description',
                          'created_by',
                          'versions',
                          'tags',
                          'url',
                          'is_public',
                          'start_date',
                          'end_date')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_image(parsed_args.id)
        image = ()
        if data:
            start_date = ts_to_isodate(data['start_date'])
            end_date = ''
            if data['end_date']:
                end_date = ts_to_isodate(data['end_date'])
            image = (
                data['id'],
                data['uuid'],
                data['name'],
                data['description'],
                data['created_by']['username'],
                '\n'.join(['{} ({})'.format(value['name'], value['id']) for value in data['versions']]),
                ', '.join([value['name'] for value in data['tags']]),
                data['url'],
                data['is_public'],
                start_date,
                end_date
            )

        return (column_headers, image)


class ImageVersionShow(ShowOne):
    """
    Show details for an image version.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ImageVersionShow, self).get_parser(prog_name)
        parser.add_argument('id', help='the image version id')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('id',
                          'name',
                          'image_name',
                          'image_description',
                          'created_by',
                          'change_log',
                          'machines',
                          'allow_imaging',
                          'start_date')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_image_version(parsed_args.id)
        image = ()
        if data:
            image = (
                data['id'],
                data['name'],
                data['image']['name'],
                data['image']['description'],
                data['user']['username'],
                data['change_log'],
                '\n'.join(['{} ({})'.format(value['provider']['name'], value['uuid']) for value in data['machines']]),
                data['allow_imaging'],
                data['start_date']
            )

        return (column_headers, image)
