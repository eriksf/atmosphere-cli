import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from atmosphere.api import AtmosphereAPI
from atmosphere.utils import ts_to_isodate


class ImageList(Lister):
    """
    List images for user.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        column_headers = ('id', 'name', 'description', 'created_by', 'versions', 'is_public', 'start_date')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url, self.app_args.api_server_timeout, self.app_args.verify_cert)
        data = api.get_images()
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
                ', '.join([value['name'] for value in data['versions']]),
                ', '.join(data['tags']),
                data['url'],
                data['is_public'],
                start_date,
                end_date
            )

        return (column_headers, image)
