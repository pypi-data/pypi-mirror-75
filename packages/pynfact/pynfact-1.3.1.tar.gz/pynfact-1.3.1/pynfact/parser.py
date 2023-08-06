# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent foldlevel=1 nowrap:
"""
Markdown translation to HTML and metadata retrieval.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT
"""
from pynfact.fileman import has_extension_md, has_extension_rst
from pynfact.parsers import ParserMd, ParserRst


class Parser:
    """Parse methods for a markup language file to generate HTML code.

    .. versionchanged:: 1.3.1b1
        Former class ``Mulang``, now it relies on the file extension to
        call one or other parser.
    """

    def __init__(self, filename, encoding='utf-8', logger=None):
        """Constructor.

        Depending on the extension, the markup parser will be a Markdown
        parser, or a reStructuredText parser.  The valid extensions are:
        ``.rst`` for reStructuredText, and ``.md`` for Markdown.

        :param filename: File from where the data is taken
        :type filename: str
        :param encoding: Encoding the input file is in
        :type encoding: str
        :param logger: Logger where to store activity in
        :type logger: logging.Logger
        """
        if has_extension_rst(filename):
            parser = ParserRst
        elif has_extension_md(filename):
            parser = ParserMd

        self.parser = parser(filename, encoding, logger=logger)

    def html(self):
        """Generate HTML from a MarkUP LANGuage file."""
        return self.parser.html()

    def metadata(self):
        """Generate metadata from a MarkUP LANGuage file."""
        return self.parser.metadata()
