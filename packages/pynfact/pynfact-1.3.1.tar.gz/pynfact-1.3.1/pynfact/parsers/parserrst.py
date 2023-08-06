# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent foldlevel=1 nowrap:
"""
reStructuredText translation to HTML and metadata retrieval.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT

.. note::
    There are some presentation and parsing problems using the docutils
    ``Writer`` class from ``html5_polyglot`` if docutils version is
    ``<0.15``.  The result is not the same, some settings are ignored,
    and the ``doctree`` seems to be interpreted in a different way
    concerning the ``docinfo`` element, way too important for the
    document metadata.  The ``fragment`` and the ``body`` parts of the
    publisher data structure seem to have also some erratic behaviour.
    It's required ``docutils>=0.15``.
"""
from docutils.core import publish_doctree, publish_parts
from docutils.nodes import docinfo
from docutils.writers.html5_polyglot import Writer


class ParserRst:
    """Generate HTML body from a reStructuredText source file.

    .. versionadded:: 1.3.1a4
        Add reStructuredText support.

    .. seealso:: :class:`ParserMd` and :mod:`parser`.
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
        :param output_format: Output HTML version
        :type output: str
        :param logger: Logger where to store activity in
        :type logger: logging.Logger
        """
        self.input_data = input_data
        self.encoding = encoding
        self.logger = logger

        self.settings = {
            'attribution': None,  # dash, parentheses
            'cloak_email_addresses': True,
            'compact_field_lists': True,
            'compact_lists': True,
            'doctitle_xform': True,
            'embed_stylesheet': False,
            'footnote_references': 'superscript',  # 'brackets'
            'initial_header_level': 2,
            'input_encoding': self.encoding,
            'language_code': 'en',
            'math_output': 'MathML',  # 'LaTeX', 'MathJax', 'HTML'
            'output_encoding': 'utf-8',
            'raw_enabled': True,
            'sectsubtitle_xform': True,
            'smart_quotes': False,
            'smartquotes_locales': True,
            'strip_comments': True,
            # 'strip_elements_with_classes': ['docinfo simple', 'docinfo'],
            # 'stylesheet_path': stylesheet_path,
            'syntax_highlight': True,
            'table_style': 'align-center',  # borderless, booktabs, align-
            'tab_width': 4,
            'toc_backlinks': False,
            'trim_footnote_reference_space': True,
        }

    def html(self):
        """Generate HTML from  a reStructuredText file.

        .. todo::
            This reStructuredText parser should import some locally
            defined roles for this application.
        """
        with open(self.input_data, "r", encoding=self.encoding) as f:
            text = f.read()

        html = publish_parts(text,
                             writer=Writer(),
                             settings_overrides=self.settings).get('fragment')
        self.logger and self.logger.debug(
            'Parsed text body of: "{}"'.format(self.input_data))

        return html

    def metadata(self):
        """Fetch metadata in a reStructuredText file.

        The metadata syntax is case insensitive and as follows::

            :author: Author A. Author
            :title: This is a title
            :subtitle: A longer, much longer title for this entry
            :cdate: 2020-03-10
            :mdate: 2020-03-19
            :tags: this, are, a, lot, of, tags
            :comments: yes

        .. note::
            This is a "cheap" approximation that I dislike.  The
            non-bibliographical fields are gotten in a different way
            than the bibliographical ones.  In docutils, the
            bibliographical fields are::

                address, author, authors, contact, copyright, date,
                field, organization, revision, status, version

            and are processed by docutils in a different way that user
            defined fields.  In order to make a dictionary that does not
            treat any field differently, we check if a field is
            biliographic (length=1), or not, (length=2).  If not, we
            store normally, if it is, we take the short representation
            and strip it from its brackets and ellipsis.

        .. todo::
            Fix how to get the fields in a much more cleaner way.
        """
        meta = dict()
        with open(self.input_data, "r", encoding=self.encoding) as f:
            text = f.read()

        doctree = publish_doctree(text,  # writer=Writer(),
                                  settings_overrides=self.settings)

        # Generate dictionary of meta information {'field': 'value'}
        for info in doctree.traverse(docinfo):
            for field in info.children:
                if len(field.children) == 1:
                    k, v = field.shortrepr().strip('<.>'), field
                    meta[str(k).lower()] = v.astext()
                elif len(field.children) == 2:
                    k, v = field.children
                    meta[k.astext().lower()] = v.astext()

        # Lowercase all the keys in the docinfo, and use the same
        # structure `{k: [v]}` as the Markdown metadata retriever
        meta = {k.lower(): [v] for k, v in meta.items()}

        # In reStructuredText, if there's no title in the meta tags, get
        # it from the document part 'title'
        if 'title' not in meta:
            meta['title'] = [doctree.get('title')]

        self.logger and self.logger.debug(
            'Parsed metadata of: "{}"'.format(self.input_data))

        return meta
