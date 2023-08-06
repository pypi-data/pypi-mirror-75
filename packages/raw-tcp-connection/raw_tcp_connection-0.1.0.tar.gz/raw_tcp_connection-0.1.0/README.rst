===============================
raw_tcp_connection
===============================

.. image:: https://travis-ci.com/romnnn/raw_tcp_connection.svg?branch=master
        :target: https://travis-ci.com/romnnn/raw_tcp_connection
        :alt: Build Status

.. image:: https://img.shields.io/pypi/v/raw_tcp_connection.svg
        :target: https://pypi.python.org/pypi/raw_tcp_connection
        :alt: PyPI version

.. image:: https://img.shields.io/github/license/romnnn/raw_tcp_connection
        :target: https://github.com/romnnn/raw_tcp_connection
        :alt: License

.. image:: https://readthedocs.org/projects/raw-tcp-connection/badge/?version=latest
        :target: https://raw-tcp-connection.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://codecov.io/gh/romnnn/raw_tcp_connection/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/romnnn/raw_tcp_connection
        :alt: Test Coverage

""""""""

Your short description here. `romnnn.github.io/raw_tcp_connection <https://romnnn.github.io/raw_tcp_connection>`_

.. code-block:: console

    $ pip install raw_tcp_connection

See the `official documentation`_ for more information.

.. _official documentation: https://raw-tcp-connection.readthedocs.io

.. code-block:: python

    import raw_tcp_connection

Development
-----------

For detailed instructions see `CONTRIBUTING <CONTRIBUTING.rst>`_.

Tests
~~~~~~~
You can run tests with

.. code-block:: console

    $ invoke test
    $ invoke test --min-coverage=90     # Fail when code coverage is below 90%
    $ invoke type-check                 # Run mypy type checks

Linting and formatting
~~~~~~~~~~~~~~~~~~~~~~~~
Lint and format the code with

.. code-block:: console

    $ invoke format
    $ invoke lint

All of this happens when you run ``invoke pre-commit``.

Note
-----

This project is still in the alpha stage and should not be considered production ready.
