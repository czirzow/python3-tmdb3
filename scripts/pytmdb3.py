#!/usr/bin/env python

from argparse import ArgumentParser
from tmdb3 import *

import sys

if __name__ == '__main__':
    # this key is registered to this library for testing purposes.
    # please register for your own key if you wish to use this
    # library in your own application.
    # http://help.themoviedb.org/kb/api/authentication-basics
    set_key('1acd79ff610c77f3040073d004f7f5b0')

    parser = ArgumentParser(
                prog = "pytmdb",
                description = "Developer Python CLI to interface with TMDB",
                epilog = "to start")

    parser.add_argument('-v', "--version",
                        help = 'Display Version.',
                        action = "store_true",
                        default = False)
    parser.add_argument('-d', '--debug',
                        help = 'Enables verbose debugging.',
                        action = "store_true",
                        default = False)
    parser.add_argument('-c', '--cache',
                        help = 'Configure which cache engine to use.',
                        choices = ['null', 'file', 'redis'],
                        default = 'redis'
                        )

    opts = parser.parse_args()
    if opts.version:
        from tmdb3.tmdb_api import __title__, __purpose__, __version__, __author__
        print(__title__)
        print("")
        print(__purpose__)
        print("Version: "+__version__)
        sys.exit(0)

    match opts.cache:
        case "nocache":
            set_cache(engine='null')
        case "file":
            print("using file cache")
            set_cache(engine='file', filename='/tmp/pytmdb3.cache')
        case "redis":
            print("using redis cache")
            set_cache(engine='redis',
                      host='localhost',
                      port=6379,
                      decode_responses=True)

    if opts.debug:
        request.DEBUG = True

    banner = 'PyTMDB3 Interactive Shell.'
    import code
    try:
        import readline, rlcompleter
    except ImportError:
        pass
    else:
        readline.parse_and_bind("tab: complete")
        banner += ' TAB completion available.'
    namespace = globals().copy()
    namespace.update(locals())
    code.InteractiveConsole(namespace).interact(banner)
