
Atmosphere CLI
==============

.. image:: https://travis-ci.org/eriksf/atmosphere-cli.svg?branch=master
   :target: https://travis-ci.org/eriksf/atmosphere-cli
   :alt: Build Status

.. image:: https://badge.fury.io/gh/eriksf%2Fatmosphere-cli.svg
   :target: https://badge.fury.io/gh/eriksf%2Fatmosphere-cli
   :alt: GitHub version

.. image:: https://readthedocs.org/projects/atmosphere-cli/badge/?version=latest
   :target: https://atmosphere-cli.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

The Atmosphere CLI is a command-line client written in Python (based on OpenStack's `cliff <https://github.com/openstack/cliff>`_ framework) for
`Atmosphere <https://github.com/cyverse/atmosphere>`_. Atmosphere is an integrative, private, self-service cloud computing
platform designed to provide easy access to preconfigured, frequently used analysis routines, relevant algorithms,
and data sets in an available-on-demand environment designed to accommodate computationally and data-intensive
bioinformatics tasks. It is currently in use on the `CyVerse <https://www.cyverse.org/>`_ and `Jetstream <https://jetstream-cloud.org/>`_
projects.

- `Package Installation (PyPI) <https://pypi.org/project/atmosphere-cli>`_
- `Documentation <https://atmosphere-cli.readthedocs.io/en/latest/>`_
- `Bugs/Issues <https://github.com/eriksf/atmosphere-cli/issues>`_

Getting Started
---------------

The Atmosphere CLI can be installed from PyPI using pip:

.. code-block:: shell

    $ pip install atmosphere-cli

There are a few ways to get help. A listing of supported commands and global options can be shown with ``--help``:

.. code-block:: shell

    $ atmo --help

There is also a ``help`` command that can be used to get help for specific commands:

.. code-block:: shell

    $ atmo help image list

(Optional) Install bash command line completion to get command hints by tabbing:

.. code-block:: shell

    $ atmo complete >> ~/.bash_aliases
    $ . ~/.bash_aliases  # add to ~/.bashrc or ~/.bash_profile to always load (Ubuntu distro's already load it)
    $ atmo <tab>
    allocation   group        identity     instance     project      size         volume
    complete     help         image        maintenance  provider     version

Configuration
-------------

The Atmosphere CLI can be configured with environment variables or command-line options. The two required variables
are **ATMO_BASE_URL**, the URL to the corresponding instance of Atmosphere, and **ATMO_AUTH_TOKEN**, the token needed
for authorization. An authorization token can be created by logging into the web client and going to the user menu
(upper right corner) and selecting *Settings -> Advanced -> Personal Access Tokens*. For instance:

.. code-block:: shell

    export ATMO_BASE_URL="https://atmo.cyverse.org"
    export ATMO_AUTH_TOKEN="xxxxxxxxxxxxxxxxxxxx"

A sample `.env` file is provided in the repo. The corresponding command-line options can also be used:

.. code-block:: shell

    --atmo-base-url <URL>
    --atmo-auth-token <TOKEN>

Contributing
------------

To contribute to development and run the included tests:

.. code-block:: shell

    # grab the repo
    $ git clone https://github.com/eriksf/atmosphere-cli
    $ cd atmosphere-cli

    # install pipenv
    $ pip install pipenv

    # install atmosphere-cli
    $ pipenv install --dev  # if multiple python versions installed, select with --python option

    # setup environment
    $ cp .env.sample .env  # edit ATMO_BASE_URL and ATMO_AUTH_URL as in Configuration section above

    # load virtual environment
    $ pipenv shell  # this also loads variables in .env to environment

License
-------

See LICENSE.txt for license information.

Authors
-------

- Erik Ferlanti <eferlanti@tacc.utexas.edu>






