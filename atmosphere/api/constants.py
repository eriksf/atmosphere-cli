"""
Constants for the Atmosphere CLI API
"""
from collections import namedtuple

ATMO_BASE_URL = 'https://local.atmo.cloud/api/v2'
ATMO_API_SERVER_VERIFY_CERT = True
ATMO_API_SERVER_TIMEOUT = None

ApiResponse = namedtuple('ApiResponse', 'ok message')
