# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent foldlevel=1 nowrap:
"""
Markdown translation to HTML and metadata retrieval.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT
"""
import markdown


class ParserMd:
    """Generate HTML body from a Markdown source file.

    .. versionchanged:: 1.2.0a1
        Implement ``logging`` instead of printing to ``stdout`` and/or
        ``stderr``.

    .. versionchanged:: 1.3.1a4
        This class, formerly ``Mulang``, now it's just a parser for
        Markdown since reStrucutedText support was added.

    .. seealso:: :class:`ParserRst` and :mod:`parser`.
    """

    def __init__(self, input_data, encoding='utf-8', logger=None):
        """Constructor.

        This class has methods to parse the markup language and get the
        information.  The logging activity is only set to debug, since
        it's not necessary to tell continuously the default activity.

        :param input_data: File from where the data is taken
        :type input_data: str
        :param encoding: Encoding the input file is in
        :type encoding: str
        :param logger: Logger where to store activity in
        :type logger: logging.Logger
        """
        self.input_data = input_data
        self.encoding = encoding
        self.logger = logger

        self.md = markdown.Markdown(
            extensions=['markdown.extensions.extra',
                        'markdown.extensions.toc',
                        'markdown.extensions.abbr',
                        'markdown.extensions.def_list',
                        'markdown.extensions.footnotes',
                        'markdown.extensions.codehilite',
                        'markdown.extensions.meta'],
            encoding=encoding,
            output_format='html5')

    def html(self):
        """Generate HTML from a Markdown file."""
        with open(self.input_data, "r", encoding=self.encoding) as f:
            text = f.read()

        html = self.md.convert(text)
        self.logger and self.logger.debug(
            'Parsed text body of: "{}"'.format(self.input_data))

        return html

    def metadata(self):
        """Fetch metadata in a Markdown file.

        The metadata syntax is case insensitive and as follows::

            author: Author A. Author
            title: This is a title
            subtitle: A longer, much longer title for this entry
            odate: 2020-03-10
            mdate: 2020-03-19
            tags: this, are, a, lot, of, tags
            comments: yes

        .. todo::
            Get the meta without generating HTML again.
        """
        with open(self.input_data, "r", encoding=self.encoding) as f:
            text = f.read()

        self.md.convert(text)
        self.logger and self.logger.debug(
            'Parsed metadata of: "{}"'.format(self.input_data))

        return self.md.Meta
