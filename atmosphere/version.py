import logging

from cliff.command import Command
from atmosphere.api import AtmosphereAPI
from atmosphere.utils import ts_to_isodate


class Version(Command):
    """Show Atmosphere API version."""

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_version()
        if data.ok:
            message = data.message
            self.app.stdout.write('Atmosphere {} {} [Built: {}]\n'.format(message['git_branch'], message['git_sha_abbrev'], ts_to_isodate(message['commit_date'], include_time=True)))
