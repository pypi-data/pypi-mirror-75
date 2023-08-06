# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent foldlevel=0 nowrap:
"""
File and path manipulation functions.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT
"""
import os

from pynfact.struri import slugify, strip_html_tags


def has_extension(filename, extension, case_sensitive=False):
    """Test if the filename has a extension in particular.

    :param filename: Filename to test
    :type filename: str
    :param extension: Extension to test against
    :type extension: str
    :return: ``True`` if the filename has the inquired extension
    :rtype: bool

    :Example:

    >>> has_extension('filename.MD', '.md', case_sensitive=True)
    False

    >>> has_extension('filename.RST', '.rst', case_sensitive=False)
    True

    >>> has_extension('filename.txt', '.md')
    False
    """
    if case_sensitive:
        return os.path.splitext(filename)[1] == extension
    else:
        return os.path.splitext(filename)[1].lower() == \
            extension.lower()


def has_extensions(filename, extensions, case_sensitive=False):
    """Check if a filename has an extension in a list of extensions.

    :param filename: Filename to test
    :type filename: str
    :param extensions: List of extensions to test against
    :type extensions: list
    :param case_sensitive: Do not considerate case if ``False``
    :type case_sensitive: bool
    :return: ``True`` if filename has a matching extension
    :rtype: bool

    :Example:

    >>> has_extensions('filename.md', ['.md', '.rst'])
    True

    >>> has_extensions('filename.rst', ['.md', '.rst'])
    True

    >>> has_extensions('filename.txt', ['.md', '.rst'])
    False
    """
    if case_sensitive:
        return os.path.splitext(filename)[1] in extensions
    else:
        return os.path.splitext(filename)[1].lower() in \
            [extension.lower() for extension in extensions]


def has_extension_md(filename):
    """Check whether a filename has a valid Markdown extension.

    :Example:

    >>> has_extension_md('filename.md')
    True

    >>> has_extension_md('filename.mDown')
    True

    >>> has_extension_md('filename.rst')
    False

    """
    return has_extensions(filename, ['.md', '.mdown', '.mkdn', '.markdown'])


def has_extension_rst(filename):
    """Check whether a filename has a valid reStructuredText extension.

    :Example:

    >>> has_extension_rst('filename.md')
    False

    >>> has_extension_rst('filename.rst')
    True

    >>> has_extension_rst('filename.reSt')
    True

    """
    return has_extensions(filename, ['.rst', '.rest', '.rtext'])


def has_extension_md_rst(filename):
    """Check if a filename has Markdown or reStructuredText extension.

    :Example:

    >>> has_extension_md_rst('filename.md')
    True

    >>> has_extension_md_rst('filename.rst')
    True

    >>> has_extension_md_rst('filename.txt')
    False
    """
    return has_extension_md(filename) or has_extension_rst(filename)


def link_to(name, prefix='', makedirs=True, justdir=False,
            index='index.html'):
    """Make a link relative path in terms of the build.

    It may return a string to the destination, and also create that path
    if it doesn't exist.

    :param name: Filename (extension will be disregarded)
    :type name: str
    :param prefix: Prefix directory to prepend the file
    :type prefix: str
    :param makedirs: If true make all needed directories
    :type makedirs: bool
    :param justdir: If true return only the link dir., not the full path
    :type justdir: bool
    :param index: Default name of file contained in the path
    :type index: str
    :return: Link path to a  ``index.html`` page
    :rtype: str

    :Example:

    >>> struri.link_to('dest', '/a/b/c', makedirs=False)
    '/a/b/c/dest/index.html'

    >>> struri.link_to('dest', 'a/b/c', makedirs=False, justdir=True)
    'a/b/c/dest'

    .. versionchanged:: 1.2.0a1
        Relocate function location from module :mod:`struri` to
        :mod:`fileman`.

    .. todo::
        Add a verbose argument, default to ``False`` (for
        compatibility), that prints status on creating the path if
        ``makedirs=True``.
    """
    dirname = slugify(strip_html_tags(os.path.splitext(name)[0]))
    path = os.path.join(prefix, slugify(dirname), index)
    if makedirs:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    return os.path.dirname(path) if justdir else path
