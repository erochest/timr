
"""\
This contains the CLI interface functions.

It handles parsing command-line arguments into an object with the options and
then forwarding everything over to the backend.
"""


__all__ = [
        'main',
        ]


import argparse
import sys


def validate_args(ap, args):
    """This checks the options objects and raises errors. """


def add_fetch_args(subparser):
    """This adds CLI arguments for the `fetch` command. """
    fetch = subparser.add_parser(
            'fetch',
            help='Download a URL and store the timings.',
            )
    fetch.add_argument(
            '-u', '--url',
            dest='url',
            required=True,
            help='The URL to test.',
            )
    fetch.add_argument(
            '-m', '--message',
            dest='message',
            help='A message for this run.',
            )
    fetch.add_argument(
            '-S', '--no-sha',
            action='store_const',
            dest='use_sha',
            default=True,
            const=False,
            help="Don't use SHA hashing to test the request response.",
            )
    fetch.add_argument(
            '-n', '--times',
            dest='n',
            type=int,
            default=4,
            help='The number of times to download the request. Default is 4.',
            )
    fetch.set_defaults(action='fetch')
    return fetch


def parse_args(argv):
    """Parse a list of command-line arguments into an object. """
    ap = argparse.ArgumentParser(
            description='Time HTTP requests and analyse the results.',
            fromfile_prefix_chars='@',
            )
    subs = ap.add_subparsers()

    add_fetch_args(subs)

    args = ap.parse_args()
    validate_args(ap, args)

    return args


def main(argv=None):
    """The main entry point for the timr script."""
    argv = argv if argv is not None else sys.argv[1:]
    args = parse_args(argv)
