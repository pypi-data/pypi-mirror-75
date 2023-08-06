# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent foldlevel=0 nowrap:
"""
Data and data structures management functions.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT

.. versionadded:: 1.3.1a3
    Separate funcionality across multiple modules.

.. versionchanged:: 1.3.1b1
    Remove funcion ``and_array_in``: it has no use for this project.
"""


def or_array_in(dictionary, *keys):
    """Check if at least one key in the array is in the dictionary.

    The funcionality is the same as the keyword ``in``, but testing each
    and every key in the array as an ``or`` operation.

    :param keys: List of keys to test against the dictionary
    :type keys: args
    :param dictionary: Dictionary
    :type dictionary: dict
    :return: Value for the matching key, or ``None``
    :rtype: mixed

    :Example:

    >>> dictionary = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

    >>> or_array_in(dictionary, ['a', 'i', 'j']
    True

    >>> or_array_in(dictionary, ['x', 'y', 'z']
    False
    """
    for key in keys:
        if key in dictionary:
            return dictionary.get(key)
    return None


def key_exists(dictionary, *keys):
    """Check if key exist in a nested dictionary.

    :param dictionary: Nested dicionary
    :type dictionary: dict
    :param keys: Keys to test agains the dictionary
    :type keys: args
    :return: ``True`` if at least one key is in the dicionary
    :rtype: bool
    :raise KeyError: If no key is in the dictionary
    """
    item = dictionary
    for key in keys:
        try:
            item = item[key]
        except KeyError:
            return False
    return True
