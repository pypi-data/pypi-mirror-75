# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent foldlevel=0 nowrap:
"""
Command line interface functions.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT
"""
import logging
import os
import shutil
import sys

from pynfact.builder import Builder
from pynfact.server import Server
from pynfact.yamler import Yamler


def set_logger(verbosity=False, error_log='pynfact.err',
               echo_log=sys.stdout):
    """Set up the system logger.

    This function starts two logs, one stream on the standard output
    (``echo_log``) where the ``verbosity`` parameter can increase the
    volume of messages; and the error log (``error_log``), saved to a
    file but only logging errors and critical errors.  Warnings, errors
    and critical errors are displayed automatically to the standard
    output.

    The parameter ``verbosity`` concerns only to what is being displayed
    on screen concordingly with the log leves of the ``logging`` module.
    These levels may be specified by an integer value or by name.  These
    are their values:

    * 10: ``logging.DEBUG``
    * 20: ``logging.INFO``
    * 30: ``logging.WARNING``
    * 40: ``logging.ERROR``
    * 50: ``logging.CRITICAL``

    The following table illustrates what is getting logged:

    +---------------+--------------+--------------+---------------+
    | ``logging.``  | ``!verbose`` |  ``verbose`` | ``error_log`` |
    +===============+==============+==============+===============+
    | ``.DEBUG``    |              |      X       |               |
    +---------------+--------------+--------------+---------------+
    | ``.INFO``     |      X       |      X       |               |
    +---------------+--------------+--------------+---------------+
    | ``.WARNING``  |      X       |      X       |               |
    +---------------+--------------+--------------+---------------+
    | ``.ERROR``    |      X       |      X       |       X       |
    +---------------+--------------+--------------+---------------+
    | ``.CRITICAL`` |      X       |      X       |       X       |
    +---------------+--------------+--------------+---------------+
    | write log to: |  ``stdout``  |  ``stdout``  |   ``file``    |
    +---------------+--------------+--------------+---------------+

    The only way to deactivate the ``error_log`` is to use the command
    line option ``-l none``, or ``--log=none``; or ``--log=/dev/null``.
    Either way, the warnings, errors and critical messages will still be
    shown on screen, for any value of ``verbosity``.  What ``verbosity``
    does is to enable or disabe the debug messages.
    Apart from that, warnings an errors may be forced to be in the
    standard output by using ``--log=/dev/stdout``, or to the standard
    error with ``--log=/dev/stderr``.

    :param verbosity: Show basic information, or also debug messages
    :type verbosity: bool
    :param error_log: Filename for the warnings and errors log
    :type error_log: str
    :param echo_log: Stream to write the default information log
    :type echo_log: _io.TextIOWrapper

    .. versionchanged:: 1.3.1a4
        If the error log is set to "None" (case insensitive), deactivate
        the log for warnings and errors.

    .. versionchanged:: 1.3.1b1
        If the error log is set as ``/dev/stdout`` or ``/dev/stderr``,
        then, instead of using a ``logging.FileHandler``, use a
        ``logging.StreamHandler`` to ``sys.stdout`` or ``sys.stderr``
        respectively.  In any other case, write to a file.

    .. versionchanged:: 1.3.1b2
        If the error log is set to ``/dev/null``, act in the same way as
        using the value "None" (case insensive), i.e., deactivate the
        warnings and errors log.
    """
    log_level = logging.DEBUG if verbosity else logging.INFO
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Default ``stdout`` handler, set by ``verbosity`` value
    echo_shandler = logging.StreamHandler(echo_log)
    echo_shandler.setLevel(log_level)
    echo_shandler.setFormatter(logging.Formatter(
        '[%(levelname)s]: %(message)s'))
    logger.addHandler(echo_shandler)

    # Errors and Critical errors handler
    if error_log.lower() != 'none' or error_log != '/dev/null':
        if error_log == '/dev/stdout':
            warning_fhandler = logging.StreamHandler(sys.stdout)
        elif error_log == '/dev/stderr':
            warning_fhandler = logging.StreamHandler(sys.stderr)
        else:
            warning_fhandler = logging.FileHandler(error_log)
        warning_fhandler.setLevel(logging.ERROR)
        warning_fhandler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s]: %(message)s'))
        logger.addHandler(warning_fhandler)

    return logger


def retrieve_config(config_file, logger=None):
    """Retrieve configuration from YAML file.

    :param config_file: YAML configuration filename
    :type config_file: str
    :param logger: Logger to pass it to the ``Yamler`` constructor
    :type logger: logging.Logger
    :return: Dictionary with the configuration written in YAML file
    :rtype: dict
    """
    config = Yamler(config_file, logger)

    site_config = {
        'uri': {
            'base': config.retrieve('base_uri', '').strip('/'),
            'canonical': config.retrieve('canonical_uri', '').rstrip('/'),
        },
        'wlocale': {
            'encoding': config.retrieve('encoding', 'utf-8'),
            'locale': config.retrieve('locale', 'en_US.UTF-8'),
            'language': config.retrieve('site_language', 'en'),
        },
        'date_format': {
            'entry': config.retrieve('datefmt_entry', "%c"),
            'home': config.retrieve('datefmt_home', "%b %_d, %Y"),
            'list': config.retrieve('datefmt_list', "%Y-%m-%d"),
        },
        'info': {
            'copyright': config.retrieve('site_copyright'),
            'site_author': config.retrieve('site_author', "Nameless"),
            'site_author_email': config.retrieve('site_author_email', ''),
            'site_description': config.retrieve('site_description'),
            'site_name': config.retrieve('site_name', "My Blog"),
        },
        'presentation': {
            'comments': config.retrieve('comments').lower() == "yes",
            'default_category':
                config.retrieve('default_category', "Miscellaneous"),
            'feed_format': config.retrieve('feed_format', "atom").lower(),
            'max_entries': config.retrieve('max_entries', 10),
        },
        'dirs': {
            'deploy': "_build",
            'extra': config.retrieve('extra_dirs')
        }
    }

    return site_config


def arg_init(logger, dst):
    """Initialize a new website structure.

    :param dst: Name of the folder containing the new website
    :type dst: str
    :param logger: Logger to pass it to the ``Yamler`` constructor
    :type logger: logging.Logger
    :raise OSError: If it's not possible to create the website folder

    .. versionchanged:: 1.3.1b
        Data files now stored in ``data`` directory.
    """
    real_path = os.path.dirname(os.path.realpath(__file__))
    src = os.path.join(real_path, 'data/initnew')
    dst = dst

    # Create new blog structure with the default values
    try:
        shutil.copytree(src, dst)
    except OSError:
        logger and logger.error(
            "Unable to initialize the website structure")
        sys.exit(11)


def arg_build(logger, config_file='config.yml'):
    """Build the static website after getting the site configuration.

    :param logger: Logger to pass it to the ``Builder`` constructor
    :type logger: logging.Logger
    """
    site_config = retrieve_config(config_file, logger)

    template_values = {
        'blog': {
            'author': site_config['info']['site_author'],
            'base_uri': site_config['uri']['base'],
            'encoding': site_config['wlocale']['encoding'],
            'feed_format': site_config['presentation']['feed_format'],
            'lang': site_config['wlocale']['language'],
            'site_name': site_config['info']['site_name'],
            'page_links': [],
        }
    }

    b = Builder(site_config, template_values, logger=logger)
    b.gen_site()


def arg_serve(logger, host='localhost', port=4000):
    """Initialize the server to listen until keyboard interruption.

    :param logger: Logger to pass it to the ``Server`` constructor
    :type logger: logging.Logger
    """
    server = Server(host, port=port, path='_build', logger=logger)
    server.serve()
