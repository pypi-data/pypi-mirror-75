# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent foldlevel=1 nowrap:
"""
Build the content.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT

.. versionchanged:: 1.3.1a4
    Include processing of reStructuredText files along with Markdown.
    Those files are detected by extension and parsed accordingly.  So,
    no extension test in this module, only in the parser.

.. versionchanged:: 1.3.1b4
    Replaced functions ``_make_entry_uri`` and ``_make_root_uri`` with
    just :func:``_make_uri``, which will behave like the former if the
    argument ``for_entry`` is set to ``True``, and the latter when set
    to ``False``.
"""
import distutils.dir_util
import filecmp
import gettext
import locale
import os
import resource
import sys
from math import ceil

from feedgen.feed import FeedGenerator
from jinja2 import Environment, FileSystemLoader

from pynfact.fileman import has_extension_md_rst, link_to
from pynfact.meta import Meta
from pynfact.parser import Parser
from pynfact.struri import slugify, strip_html_tags


class Builder:
    """Site building process manager.

    .. todo::
        Manage better the timezone, the default is always UTC, for posts
        info, and both feeds publication and modification dates.

    .. versionchanged:: 1.0.1.dev1
        Constructor takes a configuration dictionary instead of all
        parameters individually.

    .. versionchanged:: 1.0.1a1
        Input pages stored in ``pages`` directory instead of root.

    .. versionchanged:: 1.2.0a1
        Implement ``logging`` instead of printing to ``stdout`` and/or
        ``stderr``.

    .. versionchanged:: 1.3.1a4
        Allowed extension in constructor is no longer needed.  Input
        files are processed depending on their extension (Markdown or
        reStructuredText), and those are fixed.

    .. versionchanged:: 1.3.1b1
        Test of extension done by :func:`has_extension_md_rst` from
        module :mod:`fileman`.  No extensions passed as parameters nor
        defined explicitly in this class.

    .. versionchanged:: 1.3.1b2
        Feed can be disabled and will not be generated if the value of
        ``feed_format`` is neither "rss" nor "atom" (case insensitive).

    .. versionchanged:: 1.3.1b3
        Pages and entries files are read only once, put in memory and
        work from there without touching the files anymore.
    """

    def __init__(self, site_config, template_values=dict(), logger=None):
        """Constructor.

        :param config: Site configuration as multidimensional dictionary
        :type config: dict
        :param template_values: Common values in all templates
        :type template_values: dict
        :param logger: Logger where to store activity in
        :type logger: logging.Logger
        :raise localeError: If the selected locale is not supported
        """
        self.site_config = site_config
        self.template_values = template_values
        self.site_config['dirs']['deploy'] = \
            os.path.join(self.site_config.get('dirs').get('deploy'),
                         self.site_config.get('uri').get('base'))
        self.logger = logger

        # Set locale for the site.
        self.old_locale = locale.getlocale()
        try:
            self.current_locale = \
                locale.setlocale(locale.LC_ALL,
                                 self.site_config.get('wlocale').get('locale'))
        except locale.Error:
            self.logger and self.logger.error(
                "Unsupported locale setting")
            sys.exit(41)

        # Constants-like (I don't like this approach)
        # source dirs.
        self_dir = os.path.dirname(os.path.realpath(__file__))
        self.locale_dir = os.path.join(self_dir, 'data/locale')
        self.templates_dir = 'templates'
        self.builtin_templates_dir = \
            os.path.join(self.site_config.get('dirs').get('deploy'),
                         self.templates_dir)

        # dest. dirs.
        self.home_cont_dir = 'page'         # Home paginator
        self.archive_dir = 'archive'        # Archive list page
        self.categories_dir = 'categories'  # One dir. per category
        self.tags_dir = 'tags'              # One dir. per tag

        # src. & dest. dirs.
        self.pages_dir = 'pages'            # Other pages such as 'About'...
        self.entries_dir = 'posts'          # Where posts are
        self.static_dir = 'static'          # CSS, JS, &c.

        # Default values to override meta information
        self.meta_defaults = {
            'author':
                self.site_config.get('info').get('site_author'),
            'category':
                self.site_config.get('presentation').get('default_category'),
            'language':
                self.site_config.get('wlocale').get('language'),
        }

        # Generate all entries metadata, once
        self.entries_dict = self._gather_content_data().get('entries')
        self.pages_dict = self._gather_content_data().get('pages')

    def __del__(self):
        """Destructor.  Restore the locale, if changed.

        At the end of the site generation, the destructor prints the
        maximum resident set size used of this class, if the logger is
        set to show debug messages.   That is, the maximum number of
        kilobytes of physical memory that processes used simultaneously.
        """
        if sys.platform.startswith('linux') or \
                sys.platform.startswith('freebsd') or \
                sys.platform.startswith('openbsd'):
            # On Linux the result is in kilobytes.
            units = 'kilobytes'
            peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        elif sys.platform == 'darwin':
            # On OSX the result is in bytes.
            units = 'bytes'
            peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        else:
            units = ''
            peak = '(unsupported)'

        self.logger and self.logger.debug(
            'Maximum resident set size used: {} {}'.format(peak, units))

        return locale.setlocale(locale.LC_ALL, self.old_locale)

    def gen_entry(self, filename, date_format='%c'):
        """Generate a HTML entry from its markup language counterpart.

        :param filename: Markdown or reStructuredText file to parse
        :type filename: str
        :param date_format: Date format for entry
        :type date_format: str
        :return: Generated HTML
        :rtype: str
        """
        override = {'content': self._fetch_html(self.entries_dir, filename)}
        self.entries_dict.get(filename).update(override)
        values = self.template_values.copy()
        values['entry'] = self.entries_dict.get(filename)
        self._update_meta_date_format(values.get('entry'), date_format)
        outfile = self._make_output_file(
            values.get('entry').get('title'),
            self._entry_link_prefix(filename))

        return self._render_template('entry.html.j2', outfile, values)

    def gen_entries(self, date_format='%c'):
        """Generate all entries.

        :param date_format: Date format for entry
        :type date_format: str
        """
        for filename, meta in self.entries_dict.items():
            self.gen_entry(filename, date_format=date_format)

    def gen_home(self, max_entries_per_page=10, date_format='%Y-%m-%d'):
        """Generate home page, and subpages.

        :param max_entries: Max. entries per page
        :type max_entries: int
        :param date_format: Date format for home page
        :type date_format: str
        """
        entries = list()
        total_entries = 0

        for filename, meta in self.entries_dict.items():
            override = {'uri': self._make_uri(meta.get('title'),
                                              filename, for_entry=True,
                                              absolute=True)}
            self.entries_dict[filename].update(override)
            self._update_meta_date_format(meta, date_format)
            if not meta['private']:
                total_entries += 1
                entries.append(self.entries_dict[filename])

        entries = sorted(entries, key=lambda k: k.get('odate_idx'),
                         reverse=True)

        # Paginator
        total_pages = ceil(total_entries / max_entries_per_page)
        values = self.template_values.copy()

        # Generate 'index.html' even when there are no posts
        if not total_entries:
            outfile = self._make_output_file()
            self._render_template('entries.html.j2', outfile, values)
            return

        # Home page (and subsequent ones)
        for cur_page in range(1, total_pages + 1):
            min_page = (cur_page - 1) * max_entries_per_page
            max_page = cur_page * max_entries_per_page

            values['entries'] = entries[min_page:max_page]
            values['cur_page'], values['total_pages'] = \
                cur_page, total_pages

            if cur_page == 1:
                # This is the home page, the "index.html" of the site
                outfile = self._make_output_file()
            else:
                # These are the subsequent pages other than the first
                outfile = self._make_output_file(
                    str(cur_page), self.home_cont_dir)

            self._render_template('entries.html.j2', outfile, values)
            values['entries'] = {}  # reset the entries dict.

    def gen_archive(self, date_format='%c'):
        """Generate complete website archive, based on date.

        :param date_format: Date format for entry
        :type date_format: str
        """
        archive = dict()
        for filename, meta in self.entries_dict.items():
            override = {'uri': self._make_uri(meta.get('title'),
                                              filename, for_entry=True,
                                              absolute=False)}
            self.entries_dict.get(filename).update(override)
            if not meta.get('private'):
                if meta.get('oyear_idx') in archive:
                    archive[meta.get('oyear_idx')].setdefault(
                        meta.get('omonth_idx'), []).append(meta)

                    # sort entries
                    archive[meta.get('oyear_idx')][meta.get('omonth_idx')] = \
                        sorted(
                            archive[meta.get(
                                'oyear_idx')][meta.get('omonth_idx')],
                            key=lambda k: k.get('odate_idx'),
                            reverse=False)
                else:
                    archive[meta.get('oyear_idx')] = dict()
                    archive[meta.get('oyear_idx')][meta.get('omonth_idx')] = \
                        [meta]

        values = self.template_values.copy()
        values['archive'] = archive
        outfile = self._make_output_file('', self.archive_dir)
        return self._render_template('archive.html.j2', outfile, values)

    def gen_category_list(self, date_format='%c'):
        """Generate categories page (an archive sorted by category).

        :param date_format: Date format for entry
        :type date_format: str
        """
        categories = dict()
        for filename, meta in self.entries_dict.items():
            self._update_meta_date_format(meta, date_format)
            override = {'uri': self._make_uri(meta.get('title'),
                                              filename, for_entry=True,
                                              absolute=False)}
            self.entries_dict.get(filename).update(override)
            if not meta.get('private'):
                categories.setdefault(
                    meta.get('category'), []).append(meta)

                # sort entries
                categories[meta.get('category')] = \
                    sorted(categories[meta.get('category')],
                           key=lambda k: k.get('odate_idx'),
                           reverse=True)

        values = self.template_values.copy()
        values['categories'] = categories
        outfile = self._make_output_file('', self.categories_dir)
        return self._render_template('catlist.html.j2', outfile, values)

    def gen_categories(self, date_format='%c'):
        """Generate categories pages.

        :param date_format: Date format for entry
        :type date_format: str
        """
        entries_by_category = dict()
        for filename, meta in self.entries_dict.items():
            self._update_meta_date_format(meta, date_format)
            if not meta.get('private'):
                self._update_meta_date_format(meta, date_format)
                entries_by_category.setdefault(
                    meta.get('category'), []).append(meta)

        # One page for each category
        values = self.template_values.copy()
        for category in entries_by_category:
            values['category_name'] = category
            values['entries'] = entries_by_category.get(category)

            # sort entries
            values['entries'] = sorted(values.get('entries'),
                                       key=lambda k: k.get('odate_idx'),
                                       reverse=True)
            outfile = self._make_output_file(category, self.categories_dir)
            self._render_template('cat.html.j2', outfile, values)

    def gen_tags(self, date_format='%c'):
        """Generate tags pages.

        :param date_format: Date format for entry
        :type date_format: str
        """
        entries_by_tag = dict()
        for filename, meta in self.entries_dict.items():
            if not meta.get('private'):
                for tag in meta.get('tag_list'):
                    self._update_meta_date_format(meta, date_format)
                    entries_by_tag.setdefault(tag, []).append(meta)

        # One page for each tag
        values = self.template_values.copy()
        for tag in entries_by_tag:
            values['tag_name'] = tag
            values['entries'] = entries_by_tag.get(tag)
            # sort entries
            values['entries'] = sorted(values.get('entries'),
                                       key=lambda k: k.get('odate_idx'),
                                       reverse=True)
            outfile = self._make_output_file(tag, self.tags_dir)
            self._render_template('tag.html.j2', outfile, values)

    def gen_tag_cloud(self):
        """Generate tags cloud page.

        Tags will appear in different sizes depending on the their
        occurrences along the posts.  The more a tag is used, the bigger
        will be displayed.
        """
        entries_by_tag = dict()
        for filename, meta in self.entries_dict.items():
            override = {'uri': self._make_uri(meta.get('title'),
                                              filename, for_entry=True,
                                              absolute=False)}
            self.entries_dict.get(filename).update(override)
            if not meta.get('private'):
                for tag in meta.get('tag_list'):
                    entries_by_tag.setdefault(tag, []).append(meta)

        # Multipliers seq. for tag size in function of times repeated
        tagcloud_seq = [0, 14, 21, 27, 32, 38, 42, 45, 47, 48, 50, 52]

        # One page for each tag
        values = self.template_values.copy()
        values['tags'] = list()
        for tag in entries_by_tag:
            if tag:
                tagfreq = len(entries_by_tag.get(tag))
                mult = 100 + int(tagcloud_seq[-1]
                                 if tagfreq > len(tagcloud_seq)
                                 else tagcloud_seq[tagfreq - 1])
                values.get('tags').append({tag: mult})

        outfile = self._make_output_file('', self.tags_dir)
        self._render_template('tagcloud.html.j2', outfile, values)

    def gen_nav_page_links(self):
        """Update the template data to contain also all page links.

        The navigation bar contains, not all links relevant to the site,
        but also all pages without the meta descriptor ``Navigate`` set
        to "no".

        .. important::
            Since this add new data to the base template, it **must be
            invoked first**, before generating any other content.
        """
        for filename, meta in self.pages_dict.items():
            if meta.get('navigation') and not meta.get('private'):
                values = self.template_values.copy()
                values['page'] = self.pages_dict.get(filename)

                # Update base template values to get pages links in
                # nav. bar, only for those pages that have the meta tag
                # ``navigation`` set to true
                self.template_values['blog']['page_links'].append(
                    [values.get('page').get('title'),
                     values.get('page').get('uri')])

                self.logger and self.logger.info(
                    'Added page to navigation: "{}"'.format(filename))

    def gen_page(self, filename):
        """Generate a HTML page from its markup language counterpart.

        :param filename: Markdown or reStructuredText file to parse
        :type filename: str
        :return: Generated HTML
        :rtype: str
        """
        override = {'content': self._fetch_html(self.pages_dir, filename)}
        self.pages_dict.get(filename).update(override)
        values = self.template_values.copy()
        values['page'] = self.pages_dict.get(filename)
        outfile = self._make_output_file(values.get('page').get('title'))
        return self._render_template('page.html.j2', outfile, values)

    def gen_pages(self):
        """Generate all pages."""
        for filename, meta in self.pages_dict.items():
            self.gen_page(filename)

    def gen_feed(self, feed_format="atom", outfile='feed.xml'):
        """Generate blog feed.

        :param feed_format: Feed format string ('rss' or 'atom').
                            If invalid value, will default to 'atom'
        :type feed_format: str
        :param outfile: Output filename
        :type outfile: str
        """
        if feed_format.lower() != "atom" and \
           feed_format.lower() != "rss":
            return

        feed = FeedGenerator()
        # feed.logo()
        feed.id(self.site_config.get('info').get('site_name')
                if self.site_config.get('info').get('site_name')
                else self.site_config.get('uri').get('canonical'))
        feed.title(self.site_config.get('info').get('site_name')
                   if self.site_config.get('info').get('site_name')
                   else self.site_config.get('uri').get('canonical'))
        feed.subtitle(self.site_config.get('info').get('site_description')
                      if self.site_config.get('info').get('site_description')
                      else 'Feed')
        feed.author({
            'name':
                self.site_config.get('info').get('site_author'),
            'email':
                self.site_config.get('info').get('site_author_email')
        })
        feed.description(self.site_config.get('info').get('site_description'))
        feed.link(href=os.path.join(
            self.site_config.get('uri').get('canonical'),
            self.site_config.get('uri').get('base')),
            rel='alternate')
        feed.link(href=os.path.join(
            self.site_config.get('uri').get('canonical'),
            self.site_config.get('uri').get('base'),
            outfile), rel='self')
        feed.language(self.site_config.get('wlocale').get('language'))
        feed.copyright(self.site_config.get('info').get('copyright'))

        entries = list()
        for filename, meta in self.entries_dict.items():
            if not meta.get('private'):
                uri = self._make_uri(meta.get('title'), filename,
                                     for_entry=True)
                override = {
                    'content':
                        self._fetch_html(self.entries_dir, filename),
                    'full_uri':
                        os.path.join(
                            self.site_config.get('uri').get('canonical'),
                            self.site_config.get('uri').get('base'),
                            uri),
                }
                self.entries_dict.get(filename).update(override)
                entries.append(meta)

        # Sort chronologically descent
        entries = sorted(entries, key=lambda k: k.get('odate_idx'),
                         reverse=True)
        for entry in entries:
            fnew = feed.add_entry()
            fnew.id(slugify(strip_html_tags(entry.get('title'))))
            fnew.title(entry.get('title'))
            fnew.description(entry.get('content'))
            if entry.get('mdate_html'):
                fnew.updated(entry.get('mdate_html'))
                fnew.published(entry.get('mdate_html'))
            else:
                fnew.updated(entry.get('odate_html'))
            fnew.pubDate(entry.get('odate_html'))
            # , 'email':entry.get('email')})
            fnew.author({'name': entry.get('author')})
            fnew.link(href=entry.get('full_uri'), rel='alternate')

        if feed_format.lower() == "rss":
            feed.rss_file(
                os.path.join(
                    self.site_config.get('dirs').get('deploy'), outfile))
        elif feed_format.lower() == "atom":
            feed.atom_file(
                os.path.join(
                    self.site_config.get('dirs').get('deploy'), outfile))

    def gen_static(self):
        """Generate (copies) static directory."""
        src = self.static_dir
        dst = os.path.join(
            self.site_config.get('dirs').get('deploy'),
            self.static_dir)
        if os.path.exists(src):
            distutils.dir_util.copy_tree(src, dst, update=True,
                                         verbose=True)

    def gen_extra_dirs(self):
        """Generate extra directories if they exist."""
        if self.site_config.get('dirs').get('extra'):
            for extra_dir in self.site_config.get('dirs').get('extra'):
                src = extra_dir
                dst = \
                    os.path.join(self.site_config.get('dirs').get('deploy'),
                                 extra_dir)
                if os.path.exists(src):
                    distutils.dir_util.copy_tree(src, dst, update=True,
                                                 verbose=True)

    def gen_site(self):
        """Generate all website content.

        .. note::
            The first thing that has to be generated is the navigation
            links for all user defined pages.  Otherwise those links
            could be left behind on page pages.
        """
        self.logger and self.logger.info('Building static website...')

        self.gen_nav_page_links()
        self.gen_entries(self.site_config.get('date_format').get('entry'))
        self.gen_pages()
        self.gen_archive(self.site_config.get('date_format').get('list'))
        self.gen_categories(self.site_config.get('date_format').get('list'))
        self.gen_category_list(self.site_config.get('date_format').get('list'))
        self.gen_tags(self.site_config.get('date_format').get('list'))
        self.gen_tag_cloud()
        self.gen_home(self.site_config.get('presentation').get('max_entries'),
                      self.site_config.get('date_format').get('home'))
        self.gen_feed(self.site_config.get('presentation').get('feed_format'))
        self.gen_static()
        self.gen_extra_dirs()

    def _gather_content_data(self):
        """Gather all metadata from all parseable files.

        A parseable files is one with Markdown or reStructuredText valid
        extension, as described in :func:`fileman.has_extension_md_rst`.
        This way, the files will be transversed only once, and stored.

        This stores only entries information, not pages metadata, since
        pages only need to be renderer "as is".  Entries, on the other
        side, are also required to extract information in order to make
        category pages, tags, tag clouds, etc.  So, it's needed to have
        all that data in the same place.

        The structure of the return value is as follows::

            data = {
                ['entries']: {
                    'entry1.filename': Meta(entry1).as_dict(),
                    'entry2.filename': Meta(entry2).as_dict(),
                }
                ['pages']: {
                    'page1.filename': Meta(page1).as_dict(),
                    'page2.filename': Meta(page2).as_dict(),
                }
            }

        :return: Dictionary of all parseabe objects and their metadata
        :rtype: dict
        """
        # Gather entries
        entries_dict = dict()
        if os.path.isdir(self.entries_dir):
            for filename in os.listdir(self.entries_dir):
                if has_extension_md_rst(filename):
                    meta = self._fetch_meta(self.entries_dir, filename,
                                            odate_required=True)

                    override_entry = {
                        'category_uri':
                            self._make_uri(meta.category(),
                                           self.categories_dir,
                                           for_entry=False),
                        'odate_idx': meta.odate('%Y-%m-%d %H:%M:%S'),
                        'oyear_idx': meta.odate('%Y'),
                        'omonth_idx': meta.odate('%m-%d'),
                        'site_comments':
                            self.site_config.get(
                                'presentation').get('comments'),
                        'uri':
                            self._make_uri(meta.title(),
                                           filename, for_entry=True,
                                           absolute=True),
                    }
                    entries_dict[filename] = \
                        meta.as_dict(override_entry, self.meta_defaults)

        # Gather pages
        pages_dict = dict()
        if os.path.isdir(self.pages_dir):
            for filename in os.listdir(self.pages_dir):
                if has_extension_md_rst(filename):
                    meta = self._fetch_meta(self.pages_dir, filename,
                                            odate_required=False)

                    override_page = {'uri': self._make_uri(meta.title(),
                                                           for_entry=False)}
                    pages_dict[filename] = \
                        meta.as_dict(override_page, self.meta_defaults)

        return {'entries': entries_dict, 'pages': pages_dict}

    def _update_meta_date_format(self, meta, date_format):
        """Update the date format from a meta dictionary object.

        Operates on a dictionary of metainformation, output of
        :func:`Meta.as_dict``, so the key names are known.  Uses the
        two datetime information fields, ``odate_info`` for the original
        date, and ``mdate_info`` for the modified date, and rewrites in
        place the values of their string counterparts, ``odate`` and
        ``mdate``, if they are not ``None``.

        :param meta: Metainformation dictionary
        :type meta: dict
        :param date_format: New date format for ``odate`` and ``mdate``
        :type date_format: str

        .. seealso:: :func:`Meta.as_dict`
        """
        if meta.get('odate'):
            meta['odate'] = meta.get('odate_info').strftime(date_format)

        if meta.get('mdate'):
            meta['mdate'] = meta.get('mdate_info').strftime(date_format)

    def _render_template(self, template, output_data, values):
        """Render a template using Jinja2.

        :param template: Template to use
        :type template: str
        :param output_data: File where the data is saved
        :type output_data: str
        :return: Generated HTML of the output data
        :rtype: str
        """
        trans = gettext.translation('default', self.locale_dir,
                                    [self.current_locale])
        env = Environment(extensions=['jinja2.ext.i18n'],
                          loader=FileSystemLoader(
                              [self.templates_dir,
                               self.builtin_templates_dir]))
        env.install_gettext_translations(trans)
        env.globals['slugify'] = slugify  # Add `slugify` to Jinja2
        env.globals['strip_html_tags'] = strip_html_tags
        template = env.get_template(template)
        html = template.render(**values)

        # Update only those files that are different in content
        # comparing with a cache file
        with open(output_data + '~', mode="w",
                  encoding=self.site_config.get('wlocale').get('encoding')) \
                as cache_file:
            cache_file.write(html)

        if not os.path.exists(output_data) or \
           not filecmp.cmp(output_data + '~', output_data):
            with open(
                output_data, mode="w",
                encoding=self.site_config.get('wlocale').get('encoding')) \
                    as output_file:
                output_file.write(html)
            self.logger and self.logger.info(
                'Updated content of: "{}"'.format(output_data))

        # Clear cache, both in memory and space
        filecmp.clear_cache()
        os.remove(output_data + '~')

        return html

    def _fetch_markup(self, directory, filename):
        """Parse an input file depending on its extension.

        The ``Parser`` constructor detects the extension of ``filename``
        and parses its body content as well as its metadata.

        :param directory: Path to the file to be parsed
        :type directory: str
        :param filename: File to parse
        :type filename: str
        :return: Parser object
        :rtype: Parser

        .. sealso:: :class:`Parser`
        """
        return Parser(os.path.join(directory, filename),
                      encoding=self.site_config.get('wlocale').get('encoding'),
                      logger=self.logger)

    def _fetch_html(self, directory, filename):
        """Fetch HTML content out of a markup language input file.

        :param directory: Markdown or reStructuredText file directory
        :type directory: str
        :param filename: Markdown or reStructuredText file to parse
        :type filename: str
        :return: HTML content for the parsed file
        :rtype: str
        """
        return self._fetch_markup(directory, filename).html()

    def _fetch_meta(self, directory, filename, odate_required=False):
        """Fetch metadata out of a markup language input file.

        If ``odate_required`` is ``False``, the metadata is valid as
        long as it has a title; if it's ``True``, the metadata require
        to be valid, also an "origin date", or ``odate`` field.

        :param directory: Markdown or reStructuredText file directory
        :type directory: str
        :param filename: Markdown or reStructuredText file to parse
        :type filename: str
        :param odate_required: Field ``odate`` is required
        :type odate_required: bool
        :return: Parsed file metadata
        :rtype: Meta
        """
        return Meta(self._fetch_markup(directory, filename).metadata(),
                    filename, odate_required, logger=self.logger)

    def _entry_link_prefix(self, entry):
        """Compute entry final path.

        To compute the final path, it's required to take the meta
        information of that entry concerning to title and origin date.
        Let's suppose the title is "My post", and the ``odate`` set to
        "2020-04-01".  The output will be: ``posts/2020/04/01/my-post``.

        :param: Entry filename
        :type: str
        :return: Path to this entry relative to root (slugified)
        :rtype: str

        .. versionchanged:: 1.3.0a
            Set as a member method.
        """
        meta = self._fetch_meta(self.entries_dir, entry,
                                odate_required=True)

        category = meta.category(
            self.site_config.get('presentation').get('default_category'))
        odate = meta.odate('%Y-%m-%d')
        odate_arr = odate.split('-')
        path = os.path.join(str(self.entries_dir),
                            slugify(category),
                            str(odate_arr[0]),
                            str(odate_arr[1]),
                            str(odate_arr[2]))
        return path

    def _make_uri(self, name='', infix='', index='index.html',
                  for_entry=True, absolute=False):
        """Generate the link to an entry, based on the date and name.

        Link automated generation for final URIs of articles.

        :type name: Destination basename
        :param name: str
        :param infix: Appendix to the deploy directory
        :type infix: str
        :param index: Default name of the generated resource
        :type index: str
        :param absolute: Force the URI to be done from the root
        :type absolute: bool
        :param for_entry: Entry URI if ``True``, else make it from root
        :type for_entry: bool
        :return: Link to final external URI relative to root directory
        :rtype: str

        .. versionchanged:: 1.3.1b4
            Make a link either to a blog entry or to a page in just one
            method, instead of using ``_make_entry_uri`` and
            ``_make_root_uri``.
        """
        if for_entry:
            if absolute:
                path = os.path.join('/',
                                    self.site_config.get('uri').get('base'),
                                    self._entry_link_prefix(infix))

            else:
                path = self._entry_link_prefix(infix)
        else:
            path = os.path.join('/',
                                self.site_config.get('uri').get('base'),
                                infix)

        return link_to(name, path, makedirs=False, justdir=True,
                       index=index)

    def _make_output_file(self, name='', infix='', index='index.html'):
        """Return the output file link, and make required directories.

        Link automated generation for files in the deploy directory.

        :param name: Destination basename
        :type name: str
        :param infix: Appendix to the deploy directory
        :type infix: str
        :param index: Default name of the generated resource
        :type index: str
        :return: Link to the constructed path in the deploy directory
        :rtype: str
        """
        return link_to(name,
                       os.path.join(self.site_config.get('dirs').get('deploy'),
                                    infix),
                       makedirs=True, justdir=False, index=index)
