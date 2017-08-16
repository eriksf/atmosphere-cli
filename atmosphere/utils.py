import datetime
import os
import warnings
from dotenv import load_dotenv, find_dotenv
from atmosphere.api import constants


BOOLEAN_TRUE_STRINGS = ('true', 'on', 'ok', 'y', 'yes', '1')


with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    if not load_dotenv(find_dotenv()):
        if not load_dotenv(find_dotenv(usecwd=True)):
            load_dotenv(os.path.join(os.path.expanduser('~'), '.env'))


def env(arg, cast=str):
    """Find the variable in the environment, a .env file, or use a default"""

    # check if arg is in environment (or .env file)
    value = os.getenv(arg)
    if value:
        if cast is bool:
            value = value.lower() in BOOLEAN_TRUE_STRINGS
        try:
            return cast(value)
        except ValueError as e:
            raise Exception('Could not cast value from environment (or .env file) to {}'.format(cast))

    # check in constants
    return getattr(constants, arg, None)


def ts_to_isodate(date_string):
    """Convert a datetime string (UTC) into a date string in ISO format"""

    iso_date_str = None

    try:
        date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
        iso_date_str = date.date().isoformat()
    except ValueError:
        try:
            date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            iso_date_str = date.date().isoformat()
        except ValueError:
            pass

    return iso_date_str
