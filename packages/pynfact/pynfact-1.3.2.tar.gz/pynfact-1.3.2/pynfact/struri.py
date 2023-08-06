# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent foldlevel=0 nowrap:
"""
URI strings manipulation functions.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT

.. versionchanged:: 1.2.0a1
    Relocate file management functions to :mod:`fileman`.
"""
import re
from datetime import datetime

import unidecode
from dateutil import tz


def slugify(unslugged, separator='-'):
    """Slug a string.

    :param unslugged: String to slugify
    :type unslugged: str
    :param separator: Character used to separate words
    :type separator: str
    :return: Slugged string
    :rtype: str

    :Example:

    >>> slugify('Here you go a not so very long string')
    'here-you-go-a-not-so-very-long-string'

    >>> slugify('Does**this%&string=has--DASHES!?, [Also] symbols?')
    'does-this-string-has-dashes-also-symbols'

    .. versionchanged:: 1.3.1b3
        Strip beginning and ending separator characters.
    """
    return re.sub(r'\W+', separator,
                  unidecode.unidecode(
                      unslugged).strip().lower()).strip(separator)


def strip_html_tags(text):
    """Strip HTML tags in a string.

    :param text: String containing HTML code
    :type text: str
    :return: String without HTML tags
    :rtype: str

    :Example:

    >>> strip_html_tags('<div><p>This is a paragraph</div>')
    'This is a paragraph'

    >>> strip_html_tags('<em class="highlight">Highlighted</em> text')
    'Highlighted text'
    """
    return re.sub('<[^<]+?>', '', text)


def date_iso(date):
    """Convert a datetime string into ISO 8601 format.

    HTML date format agrees with ISO 8601 (see also, :RFC:`3339`), ie::

        YYYY[-MM[-DD]][Thh[:mm[:ss[.s]]]T]

    For more information:

    * `Date and Time Formats:
      <https://www.w3.org/TR/NOTE-datetime>`_
    * `Date formats:
      <https://www.w3.org/International/questions/qa-date-format>`_

    :param date: Datetime object
    :type date: datetime.datetime
    :return: Datetime formatted as ISO 8601, or empty string if invalid
    :rtype: str

    .. note::
        If the datetime object is timezone naïve, it'll be localized to
        UTC, so the feed parser, and any other function that requires
        timezone aware datetime objects, do not raise an exception.
    """
    if date and not datetime.strftime(date, '%z'):
        date = date.replace(tzinfo=tz.tzutc())
    return datetime.isoformat(date, timespec='minutes') if date else ''
