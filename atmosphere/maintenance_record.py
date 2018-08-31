import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from atmosphere.api import AtmosphereAPI
from atmosphere.utils import ts_to_isodate


class MaintenanceRecordList(Lister):
    """
    List maintenance records for Atmosphere.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(MaintenanceRecordList, self).get_parser(prog_name)
        parser.add_argument(
            '--show-all',
            action='store_true',
            dest='show_all_records',
            help='Show all maintenance records.'
        )
        return parser

    def take_action(self, parsed_args):
        column_headers = ('id', 'title', 'start_date', 'end_date')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_maintenance_records(parsed_args.show_all_records)
        records = []
        if data.ok:
            for record in data.message['results']:
                start_date = ts_to_isodate(record['start_date'])
                end_date = ts_to_isodate(record['end_date'])
                records.append((
                    record['id'],
                    record['title'],
                    start_date if start_date else record['start_date'],
                    end_date if end_date else record['end_date']
                ))

        return (column_headers, tuple(records))


class MaintenanceRecordShow(ShowOne):
    """
    Show details for a maintenance record.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(MaintenanceRecordShow, self).get_parser(prog_name)
        parser.add_argument('id', help='the maintenance record id')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('id', 'title', 'message', 'start_date', 'end_date')
        api = AtmosphereAPI(self.app_args.auth_token, base_url=self.app_args.base_url, timeout=self.app_args.api_server_timeout, verify=self.app_args.verify_cert)
        data = api.get_maintenance_record(parsed_args.id)
        record = ()
        if data.ok:
            message = data.message
            start_date = ts_to_isodate(message['start_date'])
            end_date = ts_to_isodate(message['end_date'])
            record = (
                message['id'],
                message['title'],
                message['message'],
                start_date,
                end_date
            )

        return (column_headers, record)
