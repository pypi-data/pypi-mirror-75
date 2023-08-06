# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent nowrap:
"""
Meta information processor from Markdown or reStructuredText file.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT

.. note::
    In the metainformation header of every Markdown document to be
    parsed, there may be diacritics in metainformation values (UTF-8 by
    default) but not in metainformation key names (``[A-Za-z0-9]]``).

.. versionchanged:: 1.3.1a3
    Meta tags in document header are now reduced to only English,
    although the code is set to add more.  It's possible that in next
    versions those fields will be added by importing a JSON file will
    all the translations, but for the time being, it's better to stick
    to one universal language instead of hardcoding the
    internationalization.
"""
import re
import sys

import markdown
from dateutil.parser import parse as dt_parse

from pynfact.dataman import or_array_in
from pynfact.struri import date_iso, strip_html_tags


class Meta:
    """Meta information processor.

    The ``Meta`` class also validates the metadata with the method
    :func:``Meta._is_valid``.  It seems off at first glance for a
    metadata retriever class, but it's responsability of this class
    ensure that the metadata is well-formed.

    .. versionchanged:: 1.3.1a3
        Validate source input meta tags of title (always) and date (when
        needed) raising a ``ValueError`` and passing to the logger the
        information of the error.

    .. versionchanged:: 1.3.1b1
        Filetype no longer required in the constructor, since the parser
        automatically detect the file type by checking its extension.

    .. note::
        The prefixes for date are ``o-`` for "original date", or the
        date when it was created (and not ``c-``, commonly used for
        "changed date"); and ``m-`` for modified date".
    """

    def __init__(self, meta, filename='', odate_required=False, logger=None):
        """Constructor.

        :param meta: Meta information dictionary
        :type meta: dict
        :param filename: Identifier for the file that is being tested
        :type filename: str
        :param odate_required: If ``True`` checks for the date metadata
        :type odate_required: bool
        :param logger: Logger where to store activity in
        :type logger: logging.Logger
        """
        self.meta = meta
        self.filename = filename
        self.odate_required = odate_required
        self.logger = logger
        self._is_valid()  # Validate data supplied

    def as_dict(self, override_values={}, defaults={}, date_format='%c'):
        """Return an array with all metadata.

        :param override_values: Dictionary of values to update
        :type:override_values: dict
        :param defaults: Default values if metadata value is empty
        :type defaults: dict
        :param date_format: Datetime format strings
        :type date_format: str
        :return: Dictionary of all metadata
        :rtype: dict
        """
        metadata = {
            'author': defaults['author']
            if not self.author()
            else self.author(),
            'category': defaults['category']
            if not self.category()
            else self.category(),
            'comments': self.comments(),
            'copyright': self.copyright(),
            'email': self.email(),
            'language': defaults['language']
            if not self.language()
            else self.language(),
            'mdate_html': date_iso(self.mdate_info()),
            'mdate_info': self.mdate_info(),
            'mdate': self.mdate(date_format),
            'odate_html': date_iso(self.odate_info()),
            'odate_info': self.odate_info(),
            'odate': self.odate(date_format),
            'navigation': self.navigation(),
            'private': self.private(),
            'raw_title': strip_html_tags(self.title()),
            'subtitle': self.subtitle(),
            'tag_list': self.tag_list(),
            'title': self.title(),
        }

        return metadata.update(override_values) or metadata

    def title(self):
        """Get post title as a string from post meta information.

        This function performs some validation procedures in order to
        make sure that the title is valid (ie, not empty).

        .. note::
            In order to make the title a mandatory field, it's required
            to have the ``default`` argument to ``None``, so it raises
            an exception to warn the user.

        :param default: Default value if title is empty
        :type default: str
        :return: Title field
        :rtype: str
        :raise ValueError: If the title field is empty
        """
        vs = {'title'}
        rtitle = self._parse_str_md(vs, None, ' ')

        try:
            if not rtitle:
                raise ValueError
        except ValueError:
            self.logger and self.logger.error(
                'Empty title value in "{}" metadata'.format(self.filename))
            sys.exit(33)
        else:
            return rtitle

    def subtitle(self, default=''):
        """Get post subtitle as a string from post meta information.

        Add a full stop or period at the end if the parsed string
        doesn't have one.

        :param default: Default value if title is empty
        :type default: str
        :return: Summary field
        :rtype: str
        """
        vs = {'subtitle', 'summary'}
        return self._parse_str_md(vs, default, ' ', period=True)

    def category(self, default='Miscellaneous'):
        """Get post category as a string from post meta information.

        .. note::
            A post can belong to only one category.  If the user inputs
            more than one category, the first one will be the valid one.

        :param default: Default value if category wasn't specified
        :type default: str
        :return: Value of the category field
        :rtype: str
        """
        vs = {'category', 'cat'}
        return self._parse_str_raw(vs, default, '')

    def author(self, default=''):
        """Get post author as a string from post meta information.

        :param default: Default value if author wasn't specified
        :type default: str
        :return: Value of the author field
        :rtype: str

        .. todo::
            Get author/s for pages too.

        .. todo::
            If more than one author, return a list with all authors
            instead of a string, or return always a list and process it
            later.  Use :func:`_parse_list`?
        """
        vs = {'author', 'authors'}
        return self._parse_str_raw(vs, default, ', ')

    def email(self, default=''):
        """Get post author's email as a string from meta information.

        :param default: Default value if author email wasn't specified
        :type default: str
        :return: Value of the email field
        :rtype: str
        """
        vs = {'email', 'e-mail'}
        return self._parse_str_raw(vs, default, ', ')

    def language(self, default='en'):
        """Get post language code as a string from meta information.

        :param default: Default value if language field is empty
        :type default: str
        :return: Value of the language field
        :rtype: str
        """
        vs = {'language', 'lang'}
        return self._parse_str_raw(vs, default, ', ')

    def copyright(self, default=''):
        """Get post copyright as a string from post meta information.

        :param default: Default value if title is empty
        :type default: str
        :return: Value of the copyright field
        :rtype: str
        """
        vs = {'copyright', 'license'}
        return self._parse_str_md(vs, default, ' ')

    def comments(self, default=True):
        """Get comments boolean status.

        :param default: Default value if comments tag is empty
        :type default: str
        :return: ``True`` if entry allows comments, or otherwise
        :rtype: bool
        """
        vs = {'comments'}
        return self._parse_bool(vs, default)

    def private(self, default=False):
        """Get private boolean status.

        :param default: Default value if private tag is empty
        :type default: str
        :return: ``True`` if entry is private, or ``False`` otherwise
        :rtype: bool
        """
        vs = {'private', 'priv'}
        return self._parse_bool(vs, default)

    def navigation(self, default=True):
        """Get navigation boolean status.

        :param default: Default value if navigation tag is empty
        :type default: str
        :return: ``False`` if entry is not in nav. bar, or otherwise
        :rtype: bool
        """
        vs = {'navigation', 'nav'}
        return self._parse_bool(vs, default)

    def tag_list(self, default=[]):
        """Get post tags as a list from post meta information.

        :return: List of tags
        :rtype: list
        """
        vs = {'tags'}
        return self._parse_list(vs, default)

    def tags(self):
        """Retrieve post tags as a string of comma-separated-values.

        :return: List of tags
        :rtype: str
        """
        return self._parse_cvs(self.tag_list())

    def odate_info(self):
        """Get post date as a ``datetime`` object.

        :return: Date field as object
        :rtype: datetime.datetime
        """
        vs = {'odate', 'date', 'created'}
        return self._parse_date_obj(vs)

    def odate(self, date_format='%c'):
        """Get post date as a string.

        :param date_format: Date format string
        :type date_format: str
        :return: Date field as string
        :rtype: str

        .. versionchanged:: 1.3.1a3
            Validate source input meta tags of date raising a
            ``ValueError`` and passing to the logger the information of
            the error.
        """
        try:
            if not self.odate_info() and self.odate_required:
                raise ValueError
        except ValueError:
            self.logger and self.logger.error(
                'Empty or invalid date value in "{}" metadata'.format(
                    self.filename))
            sys.exit(34)
        else:
            return self.odate_info().strftime(date_format) \
                if self.odate_info() else ''

    def mdate_info(self):
        """Get updated post date as a ``datetime`` object.

        :return: Date field as object
        :rtype: datetime.datetime
        """
        vs = {'mdate', 'update', 'updated', 'modified'}
        return self._parse_date_obj(vs)

    def mdate(self, date_format='%c'):
        """Get updated post date as a string.

        :param date_format: Date format string
        :type date_format: str
        :return: Date field as string
        :rtype: str
        :raise ValueError: If data is malformed, but ignored

        .. note:: This is not a mandatory piece of metainformation, so
            it's only taken into consideration when it's well formed and
            doesn't raise a ``ValueError``.
        """
        try:
            if not self.mdate_info():
                raise ValueError
        except ValueError:
            pass
        else:
            return self.mdate_info().strftime(date_format)

    def _is_valid(self):
        """Check if the metadata is valid.

        The metadata is considered malformed when the title (and if
        ``odate_required`` is set to ``True``, also the date) are not in
        the dictionary that is generated after parsing the file.  This
        could happen because:

        * title (or date) are missing;
        * title (or date) identifiers have invalid characters (the only
          valid ones are the ASCII character set encoded: "[A-Za-z0-9]");
        * title (or date) meta-information tag is more than one line
          long and it's not properly indented (subsequent lines require
          to be indented a minimum of four spaces).

        :raise ValueError: If the metadata is malformed

        .. versionadded:: 1.3.1a3
            Preliminary test to see if the mandatory meta tags are set,
            or otherwise an exception is thrown.
        """
        # Title is always required
        title_k = {'title'}
        try:
            if not or_array_in(self.meta, *title_k):
                raise ValueError
        except ValueError:
            self.logger and self.logger.error(
                'Missing or malformed title key in "{}" metadata'.format(
                    self.filename))
            sys.exit(31)

        # Date is required only in posts, but not in pages
        if self.odate_required:
            odate_k = {'odate', 'date', 'created'}
            try:
                if not or_array_in(self.meta, *odate_k):
                    raise ValueError
            except ValueError:
                self.logger and self.logger.error(
                    'Missing or malformed date key in "{}" metadata'.format(
                        self.filename))
                sys.exit(32)

    def _parse_str_raw(self, values, default='', joint=', '):
        """Get a value as a raw string from post meta information.

        Raw, in this context, means in plain text, with no markup
        language.

        :param values: Set of possible meta tags
        :type values: set
        :param default: Default value if no keys match
        :type default: str
        :param joint: String used as a joint between values
        :type joint: str
        :return: The value of the meta key, or the default value
        :rtype: str
        """
        value = or_array_in(self.meta, *values)
        if value:
            return joint.join(value)
        else:
            return default

    def _parse_str_md(self, values, default='', joint=' ', period=False):
        """Get value as string from metadata allowing Markdown syntax.

        It parses the Markdown code to HTML and allow this HTML for this
        particular piece of metadata, except some block elements such as
        ``p``, ``br``...

        :param values: Set of possible meta tags
        :type values: set
        :param default: Default value if no keys match
        :type default: str
        :param joint: String used as a joint between values
        :type joint: str
        :param period: Add a period at the end, if there's none
        :type period: bool
        :return: The value of the meta key, or the default value
        :rtype: str
        """
        value = or_array_in(self.meta, *values)
        if value:
            fmt = markdown.markdown(joint.join(value))
            parsed_str = re.sub(r'</*(p|br)[^>]*?>', '', fmt)
        else:
            parsed_str = default

        if period and parsed_str and not parsed_str.endswith('.'):
            parsed_str = parsed_str + '.'

        return parsed_str

    def _parse_bool(self, values, default=True):
        """Get a value as a boolean from post meta information.

        The function has two "confrontation arrays (sets)" to test
        against them the values of the intended key.  Because the meta
        tag possible values are "yes" or "no" in natural language, this
        lists have all the possible outcome, and uses one list or the
        other depending on the default value.

        :param values: Set of possible meta tags
        :type values: set
        :param default: Default value if no keys match
        :type default: str
        :return: The value of the meta key, or the default value
        :rtype: str
        """
        if default:
            bools = {'no', 'non', 'não', 'nao', 'ne', 'nein',
                     'false', '0'}
        else:
            bools = {'yes', 'sí', 'si', 'sì', 'sim', 'jes', 'oui', 'ja'
                     'true', '1'}

        value = or_array_in(self.meta, *values)
        if value:
            if any(x in map(lambda x: x.lower(), value) for x in bools):
                return not default
        return default

    def _parse_list(self, values, default=[]):
        """Get a list with all the values to the matching key.

        :param values: Set of possible meta tags
        :type values: set
        :param default: Default value if no keys match
        :type default: str
        :return: The value of the meta key as a list, or default value
        :rtype: list
        """
        value = or_array_in(self.meta, *values)
        if value:
            return [x.strip() for x in str(value[0]).split(',') if x.strip()]
        else:
            return default

    def _parse_csv(self, values, default=''):
        """Get string with values to the matching key, comma separated.

        :param values: Set of possible meta tags
        :type values: set
        :param default: Default value if no keys match
        :type default: str
        :return: The value of the meta key as a string, or default value
        :rtype: string
        """
        return ', '.join(self._dt_parse_list(values, default))

    def _parse_date_obj(self, values):
        """Get a ``datetime`` object from the metadata.

        :param values: Set of possible meta tags
        :type values: set
        :return: Datetime object
        :rtype: datetime.datetime
        """
        value = or_array_in(self.meta, *values)
        return dt_parse(''.join(value)) if value else None

    def __repr__(self):
        """Return dictionary with all metainformation."""
        return self.as_dict()

    def __str__(self):
        """Return string representation for an object of this class."""
        return str(self.meta)
