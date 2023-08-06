#!/usr/bin/env python3
# vim: set ft=python fileencoding=utf-8 tw=72 nowrap:
"""
Source distribution setup.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT
"""
from setuptools import setup, find_packages


version = '1.3.1'

with open("README.rst", "r") as fh:
    long_description = fh.read()


setup(name='pynfact',
      version=version,
      author='J. A. Corbal',
      author_email='jacorbal@gmail.com',
      url='https://github.com/jacorbal/pynfact/wiki',
      download_url='https://github.com/jacorbal/pynfact',
      project_urls={
          'Documentation': 'https://github.com/jacorbal/pynfact/wiki',
          'Funding': 'https://jacorbal.es/pynfact',
          'Source': 'https://github.com/jacorbal/pynfact',
          'Tracker': 'https://github.com/jacorbal/pynfact/issues'},
      description='Blog-oriented static website generator using '
                  'Markdown or reStructuredText.',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      platforms='any',
      license='MIT',
      keywords=['blog', 'markdown', 'restructuredtext', 'static',
                'web', 'site', 'generator'],
      py_modules=find_packages(),
      packages=['pynfact'],
      entry_points={'console_scripts': ['pynfact = pynfact.__main__:main']},
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Internet',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Site Management',
          'Topic :: Software Development :: Code Generators',
          'Topic :: Text Processing :: Markup :: HTML',
          'Topic :: Utilities',
      ],
      install_requires=[
          'feedgen >= 0.9.0',
          'docutils >= 0.15',
          'jinja2 >= 2.7',
          'markdown >= 3.0.0',
          'pygments >= 2.0.2',
          'python-dateutil >= 2.0',  # it's also a dep. of ``feedgen``
          'pyyaml >= 5.1',
          'unidecode >= 0.4.9',
      ],
      python_requires='>=3.6',
      include_package_data=True,
      )
