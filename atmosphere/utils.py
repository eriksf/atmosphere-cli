import os
import warnings
import six
from dotenv import load_dotenv, find_dotenv
from atmosphere.api import constants
from dateutil.parser import parse


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


def ts_to_isodate(date_string, include_time=False):
    """Convert a datetime string (UTC) into a date string in ISO format"""

    iso_date_str = date_string

    try:
        date = parse(date_string)
        if include_time:
            if six.PY3:
                iso_date_str = date.isoformat(timespec='seconds')
            else:
                iso_date_str = date.isoformat()
        else:
            iso_date_str = date.date().isoformat()
    except ValueError:
        pass

    return iso_date_str


def ts_to_date(date_string):
    """Convert a datetime string (UTC) into a pretty date string"""

    date_rep = date_string

    try:
        date = parse(date_string)
        date_rep = date.strftime('%b %d %H:%M:%S %Y')
    except ValueError:
        pass

    return date_rep
