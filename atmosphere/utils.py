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

