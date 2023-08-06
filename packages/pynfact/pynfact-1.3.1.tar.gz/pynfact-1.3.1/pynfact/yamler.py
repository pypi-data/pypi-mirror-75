# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent foldlevel=1 nowrap:
"""
Handle a YAML file by setting a default value when variable is not set.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT
"""
import sys

import yaml


class Yamler:
    """Handle a YAML file.

    .. versionchanged:: 1.2.0a1
        Implement ``logging`` instead of printing to ``stdout`` and/or
        ``stderr``.
    """

    def __init__(self, filename, logger=None):
        """Constructor.

        :param filename: YAML filename where to look for the config
        :type filename: str
        :raise IOError: If the configuration files cannot be read

        .. versionchanged:: 1.3.1.a2
            Update YAML loaded method to :func:`yaml.safe_load`.
        """
        self.filename = filename
        self.logger = logger
        self.fd = None
        try:
            with open(self.filename, 'r') as self.fd:
                self.config = yaml.safe_load(self.fd)
        except IOError:
            self.logger and self.logger.error(
                "Cannot read the configuration file")
            sys.exit(21)

    def __del__(self):
        """Destructor.

        Close all opened files, just to make sure, although those will
        be automatically closed.
        """
        if self.fd:
            self.fd.close()

    def __getitem__(self, key):
        """Get the value from a specific key in the configuration file.

        :param key: Key to look for
        :type key: str
        :return: The value associated to that key
        :raise: KeyError
        """
        try:
            value = self.config[key]
        except KeyError:
            self.logger and self.logger.error(
                "Key not found in configuration file")
            sys.exit(22)
        else:
            return value

    def retrieve(self, key, default_value=None):
        """Get a value from a key or sets a default value.

        :param key: Key to look for
        :type key: str
        :param default_value: Default value if key is not found
        :return: The value associated to that key, or the default value
        """
        value = self.config[key] if key in self.config else default_value
        return value
