#!/usr/bin/python3

'''Get Mapillary authentication tokens and store them.

Asks for your Mapillary password and retrieves authentication tokens
from the Mapillary API and stores them in the configuration file.

Mapillary authentication tokens do not expire so you need to run this
only once.

'''

import argparse
import getpass

from mapillary_tools import get_auth_tokens, write_config_file


def build_parser ():
    ''' Build the commandline parser. '''

    parser = argparse.ArgumentParser (
        description = __doc__,
        formatter_class = argparse.RawDescriptionHelpFormatter  # don't wrap my description
    )

    parser.add_argument (
        '-v', '--verbose', dest='verbose', action='count',
        help='increase output verbosity', default=0
    )
    parser.add_argument (
        '-u', '--user_name', required = True,
        help='your username on Mapillary'
    )
    parser.add_argument (
        '-e', '--user_email', required = True,
        help='your email on Mapillary'
    )
    return parser


if __name__ == '__main__':
    args = build_parser ().parse_args ()

    password = getpass.getpass ('Please enter your Mapillary user password : ')

    write_config_file (get_auth_tokens (args.user_name, args.user_email, password))
