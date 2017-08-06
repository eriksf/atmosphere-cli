import logging
import json

from cliff.lister import Lister
from atmosphere.api import AtmosphereAPI


class ImageList(Lister):
    """
    List images for user.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        column_headers = ('Id', 'Name', 'Description', 'Is Public?', 'Start Date')
        api = AtmosphereAPI('username', 'password')
        response = api.get_images()
        data = json.loads(response)
        images = []
        for image in data['results']:
            images.append((
                image['id'],
                image['name'],
                image['description'],
                image['is_public'],
                image['start_date']
            ))

        return (column_headers, tuple(images))
