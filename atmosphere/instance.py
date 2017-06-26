import logging

from cliff.lister import Lister


class InstanceList(Lister):
    """
    List instances for user.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        column_headers = ('Id', 'Name', 'Status', 'Start Date', 'End Date')
        return (column_headers, (
            ('1',
             'Ubuntu 12.04.5 - iPlant Base',
             'suspended',
             '2015-02-16T19:24:26Z',
             ''),)
        )
