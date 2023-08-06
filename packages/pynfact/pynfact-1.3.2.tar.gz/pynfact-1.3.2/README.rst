######
README
######

Pynfact is a simple static website generator oriented to chronological
content, like blogs or websites with historic and sequential data.  It
allows integration with external scripts, comment engines such as
Disqus, TalkYard, etc., or Google Analytics...  Theming and
configuration is possible by editing Jinja2 templates.

:Purpose:        A blog-oriented static website generator
:Latest version: **1.3.2** (2020-08-05)

.. image:: https://badge.fury.io/py/pynfact.svg
   :target: https://badge.fury.io/py/pynfact

Features
========

* *Input formats*: Markdown and reStructuredText
* *Output format*: HTML5
* *Configuration*: Jinja2 templates
* *Locale support*
* *Code syntax highlighting*
* *Atom/RSS feed generation*
* *Categories and tags*
* *Tag cloud*
* *Articles and pages*

Requirements
============

**docutils** (``docutils >= 0.1.4``):
    Python Documentation Utilities.

**feedgen** (``feedgen >= 0.9.0``):
    Feed Generator (Atom, RSS, Podcasts).

**python-dateutil** (``python-dateutil >= 2.0``):
    Extensions to the standard Python datetime module.

**Jinja2** (``jinja2 >= 2.7``):
    A small but fast and easy to use stand-alone template engine written
    in pure Python.

**Markdown** (``markdown >= 3.0.0``):
    Python implementation of Markdown.

**Pygments** (``pygments >= 1.0``):
    Syntax highlighting package written in Python.

**PyYAML** (``pyyaml >=5.1``):
    YAML parser and emitter for Python.

**Unidecode** (``unidecode >= 0.4.9``):
    ASCII transliterations of Unicode text.

Installation
============

Run::

    $ pip install pynfact

(If your default version of Python is 2.x, maybe you need to type
``pip3`` instead of ``pip``)

Usage
=====

The interaction is done by command line.  Only a few commands are
needed:

#. ``pynfact --init=<myblog>``: Create a folder with all needed content
#. Go to that directory: ``cd <myblog>``
#. Configure settings in ``config.yml``, title, name, language...
#. ``pynfact --build``: Generates the static content
#. ``pynfact --serve=localhost``: Serves locally to test the results
   (by default at ``localhost:4000``)

More details at the `GitHub project Wiki
<https://github.com/jacorbal/pynfact/wiki>`_, and at the `Qucikstart
guide <https://github.com/jacorbal/pynfact/wiki/Quickstart>`_.

Recent changes
==============

* Perform tests and upgraded to *release candidate* version (1.3.1rc2)
* Parsing read the content input files just once, and not several times
* Logging errors now can be redirected to ``stderr``, ``stdout`` and not
  only to a file, using the command line ``--log`` (or ``-l``)
* Refactor document parser and metadata gathering
* Perform tests and upgraded to *beta* version (1.3.1b1)
* Add reStructuredText support (``docutils``)
* Validate  input metadata (titles, and dates if required) in ``Meta``
* Update ``setup.py`` to fix missing dependency ``PyYAML``
* CLI interface with ``argparser`` and more modularized
* Improve code readability to comply with :PEP:`8` and :PEP:`257`
* Generate pages slugs as posts, i.e, from the title, not the filename
* Add logging support using ``logging``
* Put every page in the same directory: ``pages``
* Deploy as Python package at PyPI:
  `<https://pypi.org/project/pynfact/>`_
* Add Esperanto locale (``eo``)
* Simplify ``Builder``  class constructor, now takes a configuration
  dictionary, sorted semantically
* Replace ``pyatom`` for ``feedgen`` to generate RSS/Atom syndication
  feeds

Refer to ``CHANGELOG`` file for more details.

Why this name?
==============

Granted it will be used on the "web", the word "log" in Latin may be
translated as *INdicem FACTorum*, hence *InFact* or **-nFact** to be
more easily pronounceable when prepending the prefix *py-*, an indicator
of the programming language where it has been developed.

Also, *pyblog*, *pyblic*, *pyweblog* and many other cool names were
already taken.

Contributing
============

Bugs
~~~~

This project is still in development, so there are probably lots of bugs
that need to be fixed before deploying a stable release.  If you find a
bug, please, report it at the `GitHub issue tracker`_.

License
=======

**PynFact!** is distributed under the `MIT License`_.  Read the
``LICENSE`` file embeeded in this project for more information.


.. .. _pynfact_logo: logo.png

.. _`GitHub issue tracker`: https://github.com/jacorbal/pynfact/issues
.. _r/PynFact: https://www.reddit.com/r/PynFact/
.. .. _`MIT License`: https://opensource.org/licenses/MIT
.. _`MIT License`: https://github.com/jacorbal/pynfact/blob/master/LICENSE

