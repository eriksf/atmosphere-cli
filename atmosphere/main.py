import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager
from pbr.version import VersionInfo
from atmosphere import utils

version_info = VersionInfo('atmosphere-cli')


class AtmosphereApp(App):

    logger = logging.getLogger(__name__)

    def __init__(self):
        super(AtmosphereApp, self).__init__(
            description='Atmosphere CLI',
            version=version_info.version_string(),
            command_manager=CommandManager('atmosphere.cli'),
            deferred_help=True,
        )

    def build_option_parser(self, description, version):
        parser = super(AtmosphereApp, self).build_option_parser(description, version)

        # override base_url
        parser.add_argument(
            '--atmo-base-url',
            metavar='<atmosphere-base-url>',
            dest='base_url',
            default=utils.env('ATMO_BASE_URL'),
            help='Base URL for the Atmosphere API (Env: ATMO_BASE_URL)'
        )

        # atmosphere api auth token
        parser.add_argument(
            '--atmo-auth-token',
            metavar='<atmosphere-auth-token>',
            dest='auth_token',
            default=utils.env('ATMO_AUTH_TOKEN'),
            help='Token used to authenticate with the Atmosphere API (Env: ATMO_AUTH_TOKEN)'
        )

        return parser

    def initialize_app(self, argv):
        super(AtmosphereApp, self).initialize_app(argv)
        self.logger.debug('Starting app, options: {}'.format(self.options))


def main(argv=sys.argv[1:]):
    atmoApp = AtmosphereApp()
    return atmoApp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
