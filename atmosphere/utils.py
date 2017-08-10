import datetime
import os
import warnings
from dotenv import load_dotenv, find_dotenv
from atmosphere.api import constants


with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    if not load_dotenv(find_dotenv()):
        if not load_dotenv(find_dotenv(usecwd=True)):
            load_dotenv(os.path.join(os.path.expanduser('~'), '.env'))


def env(arg):
    """Find the variable in the environment, a .env file, or use a default"""

    value = os.getenv(arg, default=getattr(constants, arg, None))
    return value


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
