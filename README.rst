``cweather``: Weather for your Command Line
===========================================

This is a really simple script that gives you a pretty and colorful display of
the weather on your command line. Presumably, it would be useful to put in your
login script or MOTD so that you can see the weather when you log into a
terminal.

:Author: Jack Rosenthal
:Requires: Python 3.4 or greater, Requests
:License: MIT
:Contributing: See ``CONTRIBUTING.rst``

Installation
~~~~~~~~~~~~

Install using ``pip``::

    pip install cweather

.. note::

    Pass the ``--user`` flag to ``pip`` if you would like to install for your
    local user.

Usage
~~~~~

``cweather [-h] [--api-key API_KEY] [--timeout TIMEOUT] [--no-color] [location]``

-h, --help         show this help message and exit
--api-key API_KEY  Wunderground API key, defaults to ``WUNDERGROUND_API_KEY``
                   in your environment, or some random one that might work if
                   unset
--timeout TIMEOUT  Timeout for connection
--no-color         No colors, default if ``TERM`` is ``vt100``

``location`` specifies a named location (e.g., ``Golden, CO``) or a postal
code, and will default to the ``LOCATION`` environment variable, or 80401
(Golden, CO) if unset.
