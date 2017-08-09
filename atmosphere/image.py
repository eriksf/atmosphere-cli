import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from atmosphere.api import AtmosphereAPI


class ImageList(Lister):
    """
    List images for user.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        column_headers = ('Id', 'Name', 'Description', 'Created By', 'Version(s)', 'Is Public?', 'Start Date')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url)
        data = api.get_images()
        images = []
        for image in data['results']:
            images.append((
                image['id'],
                image['name'],
                image['description'],
                image['created_by']['username'],
                ', '.join([value['name'] for value in image['versions']]),
                image['is_public'],
                image['start_date']
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
        column_headers = ('Id', 'Name', 'Description', 'Created By', 'Version(s)', 'Is Public?', 'Start Date')
        api = AtmosphereAPI(self.app_args.auth_token, self.app_args.base_url)
        data = api.get_image(parsed_args.id)
        image = ()
        if data:
            image = (
                data['id'],
                data['name'],
                data['description'],
                data['created_by']['username'],
                ', '.join([value['name'] for value in data['versions']]),
                data['is_public'],
                data['start_date']
            )

        return (column_headers, image)
