#!/usr/bin/env python3
# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent foldlevel=0 nowrap:
"""
Main entry point.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT
"""
import argparse
import sys

from pynfact.cli import arg_build, arg_init, arg_serve, set_logger

try:
    import colored_traceback.auto
    colored_traceback.add_hook(always=True)
except ImportError:
    pass


def main():
    """Manage the command line arguments.

    .. versionchanged:: 1.2.0a1
        Implement ``logging`` instead of printing to ``stdout`` and/or
        ``stderr``.

    .. versionchanged:: 1.3.1a1
        Retrieve arguments by using :mod:`argparse`.

    .. versionchanged:: 1.3.1a2
        Move functions to :mod:`cli` and renamed file as ``main.py``.

    .. versionchanged: 1.3.1rc3
        Add option to change configuration file and modified the
        requirements for main options.  Now ``--serve`` defaults to
        ``localhost`` when no host is specified, and it can be used in
        conjuction with ``--build``.
    """
    parser = argparse.ArgumentParser(description=""
                                     "PynFact!: "
                                     "Static website generator from Markdown "
                                     "and reStructuredText to HTML5",
                                     prog="pynfact",)
    # formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    rgroup = parser.add_mutually_exclusive_group()  # required=True)

    rgroup.add_argument('-i', '--init', default=None,
                        metavar='<site>',
                        help="initialize a new website structure")
    rgroup.add_argument('-b', '--build', action='store_true',
                        help="parse input files and build the website")
    parser.add_argument('-s', '--serve',  # nargs='?',
                        # default='localhost', const='localhost',
                        metavar='<host>',
                        help="set host where to serve the website "
                             "(localhost)")
    parser.add_argument('-p', '--port', default=4000,
                        metavar='<port>', type=int,
                        help="set port to listen to when serving (4000)")
    parser.add_argument('-c', '--config',
                        default='config.yml',
                        metavar='<config_file>',
                        help="use a config file other than the default "
                             "(config.yaml)")
    parser.add_argument('-l', '--log', default='pynfact.err',
                        metavar='<log_file>',
                        help="set file where to log errors "
                             "(pynfact.err)")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="increase output verbosity")

    # Print help if no arguments supplied
    args = parser.parse_args(None if sys.argv[1:] else ['--help'])

    # Set the logger
    logger = set_logger(args.verbose, error_log=args.log)

    # Process arguments
    if args.init:
        arg_init(logger, args.init)
    elif args.build:
        arg_build(logger, config_file=args.config)

    if args.serve:
        arg_serve(logger, args.serve, int(args.port))


# Main entry
if __name__ == '__main__':
    main()
