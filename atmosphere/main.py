import sys

from cliff.app import App
from cliff.commandmanager import CommandManager
from pbr.version import VersionInfo

version_info = VersionInfo('atmosphere-cli')


class AtmosphereApp(App):

    def __init__(self):
        super(AtmosphereApp, self).__init__(
            description='Atmosphere CLI',
            version=version_info.version_string(),
            command_manager=CommandManager('atmosphere.cli'),
            deferred_help=True,
        )


def main(argv=sys.argv[1:]):
    atmoApp = AtmosphereApp()
    return atmoApp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
