# -*- coding: utf-8 -*-
import os
from tests.mock_server import get_free_port, start_mock_server


# -----------------------------------------------------------------------------
# HOOKS:
# -----------------------------------------------------------------------------
def before_all(context):
    setup_python_path()
    setup_context_with_global_params_test(context)

    mock_server_port = get_free_port()
    mock_users_base_url = 'http://localhost:{port}'.format(port=mock_server_port)
    os.environ['ATMO_BASE_URL'] = mock_users_base_url
    server = start_mock_server(mock_server_port)
    context.mock_users_base_url = mock_users_base_url
    context.server = server


def after_all(context):
    context.server.shutdown()
    os.environ['ATMO_BASE_URL'] = ''


# -----------------------------------------------------------------------------
# SPECIFIC FUNCTIONALITY:
# -----------------------------------------------------------------------------
def setup_context_with_global_params_test(context):
    context.global_name = "env:Alice"
    context.global_age = 12


def setup_python_path():
    # -- NEEDED-FOR: formatter.user_defined.feature
    PYTHONPATH = os.environ.get("PYTHONPATH", "")
    os.environ["PYTHONPATH"] = "." + os.pathsep + PYTHONPATH
